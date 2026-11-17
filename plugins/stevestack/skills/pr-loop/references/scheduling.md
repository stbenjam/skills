# PR Loop Scheduling

## Select a backend and create schedules (Step 1.7)

**Prefer native T3 scheduled tasks via MCP.** Look for
`schedule_task`, `list_scheduled_tasks`, `update_scheduled_task`,
and `delete_scheduled_task` (tool names may have a prefix such
as `mcp__t3_code__`). If they are missing from the tool catalog,
attempt MCP discovery or one read-only `list_scheduled_tasks`
call before concluding they are absent. Use native `CronList`,
`CronCreate`, and `CronDelete` **only when T3 scheduling tools
are absent**. A runtime error from a present T3 tool is not a
reason to switch to Cron*: inspect/retry it and report persistent
errors. If neither backend is available, notify the user that
scheduling is unavailable and continue the current CI/review cycle.
Do not substitute unrelated page/site automations; follow Step 5.2's handoff.

Use the selected backend throughout the run, including project
overrides. Maintain two recurring schedules:

1. **Dynamic** — initially every 10 minutes; adjust its interval
   as the backoff schedule progresses (Step 5.3).
2. **Watcher** — every 8 hours, as a safety net if the dynamic
   schedule fails. Keep it until termination (Step 5.4).

Identify each schedule by the full PR URL and its role, e.g.
`pr-loop dynamic: <pr-url>` and `pr-loop watcher: <pr-url>`.
List existing schedules first and reuse matching ones; create
only missing roles. Include the PR URL, worktree path, original
start timestamp (Step 1.5), and instructions to resume this skill
in each prompt. On resumed runs, preserve that timestamp so the
backoff and one-week limit do not restart.

**T3:** use `list_scheduled_tasks` in the current project (omit
`projectId`) and retain each returned `scheduledTaskId`. Create
missing schedules with `schedule_task`, `bindToCurrentThread: true`,
and a structured `schedule` object, never JSON text:

- Dynamic: `{"type":"interval","everyMs":600000}`
- Watcher: `{"type":"interval","everyMs":28800000}`

Give each creation a distinct `clientRequestId` and reuse it
when retrying that creation. If a response is uncertain, list
tasks before retrying to avoid duplicates. Report the returned
`nextRunAt` to the user.

**Cron* fallback:** use `CronList` to find matching jobs and
`CronCreate` to create the missing dynamic/watcher schedules.
Retain their job IDs for rescheduling and cleanup.

## Reschedule (Step 5.2)

Adjust only the **dynamic** schedule to the appropriate interval:

- **T3:** call `update_scheduled_task` with its `scheduledTaskId`
  and `schedule: {"type":"interval","everyMs":<interval-ms>}`.
  Convert minutes/hours from Step 5.3 to milliseconds. Reuse the
  task rather than deleting and recreating it.
- **Cron* fallback:** find the dynamic job with `CronList`,
  delete it with `CronDelete`, and recreate it with `CronCreate`
  at the new interval; retain the replacement ID.

Leave the 8-hour watcher schedule unchanged.

## Cleanup (Step 5.4)

Delete both the dynamic and watcher schedules using the selected
backend: T3 `delete_scheduled_task` with each `scheduledTaskId`, or
fallback `CronDelete` with each job ID. If IDs were lost, list
schedules and match this PR's URL and roles; leave unrelated schedules
alone.
