---
name: task-walkthrough
description: Walk through a Terminal-Bench task, internal eval, or benchmark task PR for a competent CS engineer, explain its verifier and review rubric, then check understanding with one applied question at a time. Use when the user wants to understand or present a task before reviewing it.
---

# Task Walkthrough

Help the user understand what a task tests, how success is measured, and whether
the assessment is meaningful. Assume a competent CS engineer who may be new to
the domain. Present the walkthrough first, then conduct a serial knowledge check.
This request authorizes inspection and explanation; solving the task, editing
the task, and posting a review are separate actions.

## Inspect the task

Identify the task directory, repository revision, and PR if supplied. If the
target cannot be inferred from context, ask for it. For a PR, inspect the head
revision and relevant surrounding code, including unchanged verifier helpers.
Follow the repository's instructions and review guidance.

Read the task prompt, environment and fixtures, reference solution if available,
verifier entrypoint and helpers, and task metadata. Locate applicable `REVIEW.md`,
rubrics, contribution guidance, and benchmark requirements. Trace how the harness
sets up the task, exposes inputs to the agent, collects its work, and computes
the final score. Distinguish agent-visible inputs from reference answers and
held-out tests. State any unavailable artifacts or harness behavior that limit
the analysis; do not fill gaps with assumed framework defaults.

Prefer static inspection. If execution is necessary to resolve a material
uncertainty, first inspect what the command runs and use an authorized isolated
environment. A walkthrough does not require running unknown task or verifier
code on the host.

## Explain and assess

Use [the summary template](references/summary-template.md) to present the
following findings. Keep the first explanation brief; put supporting detail
beside the relevant assessment or code link.

### Purpose and domain

State what the agent must accomplish, the field or knowledge-work domain, and
the expected deliverable. Give a 1–2 sentence domain explanation for a competent
CS engineer; define unfamiliar terms by connecting them to familiar concepts.
Use a small concrete example when it clarifies the underlying operation.

### Difficulty for current frontier models

Separate **measured evidence** from **reasoned estimates**. Look for task-specific
evaluation results, model/version, date, harness, tool access, time/token budget,
number of trials, and failure traces. Do not treat an aggregate benchmark score
as evidence that this particular task is hard.

If identifying the latest public frontier models or citing current capability
claims, verify them against current primary sources. Keep private task content
out of public searches. If results or current sources are unavailable, label the
assessment as an estimate and name the missing evidence. Do not invent pass rates
or claim to have run models.

Explain the actual bottlenecks: domain reasoning, multi-step dependencies,
implementation, tool use, debugging, context management, or resource constraints.
Distinguish those from ambiguity, broken setup, inaccessible inputs, or verifier
quirks that make a task fail without demonstrating the intended skill. State a
difficulty judgment, confidence, and what evidence would change it.

### Realism

Assess whether the objective, supplied artifacts, constraints, and deliverable
resemble work a practitioner would do. Use a nuanced judgment such as realistic,
realistic core with artificial constraints, or primarily a puzzle. Identify
specific artificial friction or traps and whether they test a useful skill.
Do not infer realism from difficulty or equate every simplified benchmark with
a contrived task.

### Task flow

Produce a high-level diagram using Mermaid when the host supports rendering;
otherwise use ASCII. Label arrows with requests, inputs, and outputs. Include
the user/task prompt, harness/environment, agent work, resulting artifacts or
program, verifier, and score. Show reference data or hidden inputs separately,
including which components can access them. Adapt the topology to the actual
task rather than forcing every task into a single linear pipeline.

### Verifier and isolation

Explain the concrete checks and how they become a score or pass/fail result:

- Does the verifier inspect pre-produced artifacts, execute agent-written code,
  query a changed environment/service, or combine these approaches? Reading or
  parsing a generated source file is different from running it.
- What inputs, reference answers, invariants, tolerances, and hidden cases does
  it use? What would pass despite missing the intended skill, or fail despite
  satisfying the prompt? Label untested bypasses as hypotheses.
- Where does agent code run, under what identity, and with which filesystem,
  network, credential, and resource access? Identify actual isolation mechanisms
  and limits in the task or harness. A container declaration or subprocess call
  alone does not establish a secure sandbox. Distinguish task-local evidence
  from harness guarantees and unknowns.

### Review guidelines

Check the task against every applicable criterion in the available review
guidelines or rubric. Use **meets**, **falls short**, **unknown**, or **not
applicable**, with evidence and the consequence of each shortfall. Suggest a
specific correction when useful; do not silently fix the task. A reference
solution passing does not establish compliance with the full rubric.

If no guidance is found, say so and label any quality assessment as your own
judgment. Do not fabricate a rubric or certify compliance you cannot verify.

### Key code sections

Select the **3–5 most useful sections**, typically the task contract, setup or
fixtures, central domain operation/reference solution, verifier, and scoring or
execution boundary. Explain what each does and why the user should read it.
Choose substantive sections rather than every changed file. Verify file and
line numbers against the inspected revision.

For a GitHub PR, use links to the inspected repository and immutable head commit
with line anchors (`blob/<head-sha>/<path>#Lx-Ly`). Link unchanged dependencies at
their inspected revision too. Otherwise use clickable local file links supported
by the host, or plain `path:line` references when file linking is unavailable.
If fewer than three substantive sections are accessible, explain that limit.

## Check understanding, one question at a time

After the walkthrough, ask **3–5 distinct applied questions**, serially and
individually. Prepare the expected reasoning privately; do not show an answer
key or list the upcoming questions. Cover the task's goal/domain operation,
input-to-output reasoning, verifier behavior, and an important limitation or
tradeoff. Ground questions in the inspected task.

Ask the first question and wait for the user's answer before asking the next.
Use a single-question input tool if available; otherwise end the response with
that one question and resume on the next user turn. Do not put multiple
questions or subquestions into one prompt, queue questions asynchronously, or
simulate the user's replies. Prefer free-form reasoning over recognition of a
preselected answer.

Use predictions, changed inputs, counterexamples, or short scenarios that require
applying the explanation. For example, for a task that estimates a transformation
from noisy observations, ask what should happen when one observation becomes a
large outlier and why. Avoid vocabulary quizzes, filename recall, and questions
answered by copying a sentence from the summary.

Evaluate the reasoning, accepting equivalent explanations without requiring
domain jargon. For a correct answer, briefly connect it to the task and proceed
to the next question. For a partial or incorrect answer, identify what was right,
give a short corrective explanation with a concrete example, then ask one
focused follow-up using a changed example. Wait for that reply before moving on;
the correction itself is not evidence of understanding. Repair questions do not
count as new topic coverage.

Finish when the user demonstrates a working understanding of the essential
concepts across the 3–5 questions, or chooses to stop. Give a brief recap of what
they understand and any remaining gap. If they stop early, record what remains
unchecked rather than declaring a pass. Honor requests to skip the check or
revisit the explanation.
