#!/usr/bin/env python3
"""Fetch unresolved review comments from trusted reviewers and authorized bots on a GitHub PR.

Usage: python3 fetch_comments.py <owner/repo> <pr_number>

Outputs JSON with unresolved review threads, review summary bodies, and
top-level issue comments from collaborators, members, owners, and hardcoded bot accounts.
Comments from anyone else are listed in `untrusted_comments` by author and
URL only; their text is omitted so it never reaches the agent.
"""

import json
import re
import subprocess
import sys
import time

TRUSTED_ASSOCIATIONS = {"COLLABORATOR", "CONTRIBUTOR", "OWNER", "MEMBER"}

AUTHORIZED_BOTS = {
    "coderabbitai[bot]",
    "claude[bot]",
    "copilot[bot]",
    "copilot-pull-request-reviewer[bot]",
    "Copilot",
    "codex[bot]",
    "devin-ai-integration[bot]",
    "openai-codex[bot]",
    "codecov[bot]",
    "dependabot[bot]",
    "renovate[bot]",
    "github-actions[bot]",
}

RATE_LIMIT_SLEEP = 0.3

_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_HTML_COMMENT_UNTERMINATED_RE = re.compile(r"<!--.*", re.DOTALL)


def strip_html_comments(text):
    text = _HTML_COMMENT_RE.sub("", text)
    text = _HTML_COMMENT_UNTERMINATED_RE.sub("", text)
    return text.strip()


def gh_graphql(query, variables=None):
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    if variables:
        for k, v in variables.items():
            cmd.extend(["-f", f"{k}={v}"])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"GraphQL query failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def gh_rest(endpoint):
    result = subprocess.run(
        ["gh", "api", endpoint, "--paginate"],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"REST API failed: {result.stderr.strip()}")
    text = result.stdout.strip()
    if not text:
        return []
    if text.startswith("[") and "][" in text:
        text = text.replace("][", ",")
    return json.loads(text)


def is_trusted(author_login, author_association):
    if author_association in TRUSTED_ASSOCIATIONS:
        return True
    if author_login in AUTHORIZED_BOTS:
        return True
    if f"{author_login}[bot]" in AUTHORIZED_BOTS:
        return True
    return False


def untrusted_entry(kind, author, author_type, assoc, url):
    return {
        "kind": kind,
        "author": author,
        "author_type": author_type,
        "author_association": assoc,
        "url": url,
    }


def fetch_review_threads(owner, repo, pr_number, untrusted):
    threads = []
    has_next = True
    cursor = None

    while has_next:
        after_clause = f', after: "{cursor}"' if cursor else ""
        query = """
        query {
          repository(owner: "%s", name: "%s") {
            pullRequest(number: %d) {
              reviewThreads(first: 50%s) {
                pageInfo { hasNextPage endCursor }
                nodes {
                  id
                  isResolved
                  isOutdated
                  comments(first: 50) {
                    nodes {
                      id
                      databaseId
                      author { __typename login }
                      authorAssociation
                      body
                      path
                      line
                      createdAt
                      url
                    }
                  }
                }
              }
            }
          }
        }
        """ % (owner, repo, pr_number, after_clause)

        data = gh_graphql(query)
        pr_data = data.get("data", {}).get("repository", {}).get("pullRequest", {})
        thread_data = pr_data.get("reviewThreads", {})
        page_info = thread_data.get("pageInfo", {})

        for node in thread_data.get("nodes", []):
            if node["isResolved"]:
                continue

            comments = []
            untrusted_count = 0
            for c in node.get("comments", {}).get("nodes", []):
                author = c.get("author", {}).get("login", "unknown")
                assoc = c.get("authorAssociation", "")
                if not is_trusted(author, assoc):
                    untrusted_count += 1
                    untrusted.append(untrusted_entry(
                        "review_comment", author,
                        (c.get("author") or {}).get("__typename", ""),
                        assoc, c.get("url", ""),
                    ))
                    continue
                comments.append({
                    "id": c.get("databaseId"),
                    "node_id": c.get("id"),
                    "author": author,
                    "author_type": (c.get("author") or {}).get("__typename", ""),
                    "author_association": assoc,
                    "body": strip_html_comments(c.get("body", "")),
                    "path": c.get("path", ""),
                    "line": c.get("line"),
                    "created_at": c.get("createdAt", ""),
                    "url": c.get("url", ""),
                })

            if comments:
                thread = {
                    "thread_id": node["id"],
                    "thread_node_id": node["id"],
                    "resolved": False,
                    "is_outdated": node.get("isOutdated", False),
                    "comments": comments,
                }
                if untrusted_count:
                    thread["untrusted_comments_excluded"] = untrusted_count
                threads.append(thread)

        has_next = page_info.get("hasNextPage", False)
        cursor = page_info.get("endCursor")
        time.sleep(RATE_LIMIT_SLEEP)

    return threads


def fetch_issue_comments(owner, repo, pr_number, untrusted):
    endpoint = f"repos/{owner}/{repo}/issues/{pr_number}/comments"
    raw = gh_rest(endpoint)

    comments = []
    for c in raw:
        author = c.get("user", {}).get("login", "unknown")
        assoc = c.get("author_association", "")
        if not is_trusted(author, assoc):
            untrusted.append(untrusted_entry(
                "issue_comment", author, (c.get("user") or {}).get("type", ""),
                assoc, c.get("html_url", ""),
            ))
            continue
        comments.append({
            "id": c.get("id"),
            "node_id": c.get("node_id", ""),
            "author": author,
            "author_type": (c.get("user") or {}).get("type", ""),
            "author_association": assoc,
            "body": strip_html_comments(c.get("body", "")),
            "created_at": c.get("created_at", ""),
            "url": c.get("html_url", ""),
        })

    return comments


def fetch_reviews(owner, repo, pr_number, untrusted):
    endpoint = f"repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    raw = gh_rest(endpoint)

    reviews = []
    for r in raw:
        author = (r.get("user") or {}).get("login", "unknown")
        assoc = r.get("author_association", "")
        body = strip_html_comments(r.get("body") or "")
        if not body:
            continue
        if not is_trusted(author, assoc):
            untrusted.append(untrusted_entry(
                "review", author, (r.get("user") or {}).get("type", ""),
                assoc, r.get("html_url", ""),
            ))
            continue
        reviews.append({
            "id": r.get("id"),
            "node_id": r.get("node_id", ""),
            "author": author,
            "author_type": (r.get("user") or {}).get("type", ""),
            "author_association": assoc,
            "state": r.get("state", ""),
            "body": body,
            "submitted_at": r.get("submitted_at", ""),
            "url": r.get("html_url", ""),
        })

    return reviews


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <owner/repo> <pr_number>", file=sys.stderr)
        sys.exit(1)

    repo_full = sys.argv[1]
    pr_number = int(sys.argv[2])

    if "/" not in repo_full:
        print("Error: repo must be in owner/repo format", file=sys.stderr)
        sys.exit(1)

    owner, repo = repo_full.split("/", 1)

    untrusted = []

    try:
        threads = fetch_review_threads(owner, repo, pr_number, untrusted)
    except RuntimeError as e:
        print(json.dumps({"error": f"Failed to fetch review threads: {e}"}))
        sys.exit(1)

    time.sleep(RATE_LIMIT_SLEEP)

    try:
        issue_comments = fetch_issue_comments(owner, repo, pr_number, untrusted)
    except RuntimeError as e:
        print(json.dumps({"error": f"Failed to fetch issue comments: {e}"}))
        sys.exit(1)

    time.sleep(RATE_LIMIT_SLEEP)

    try:
        reviews = fetch_reviews(owner, repo, pr_number, untrusted)
    except RuntimeError as e:
        print(json.dumps({"error": f"Failed to fetch reviews: {e}"}))
        sys.exit(1)

    output = {
        "pr": f"{repo_full}#{pr_number}",
        "unresolved_threads": threads,
        "reviews": reviews,
        "issue_comments": issue_comments,
        "untrusted_comments": untrusted,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
