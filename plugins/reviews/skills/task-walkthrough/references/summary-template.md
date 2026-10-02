# Walkthrough summary template

Use this structure for the initial presentation. Replace bracketed prompts with
task-specific findings, remove empty scaffolding, and keep detail proportional
to the task. This template does not include the knowledge-check answer key.

## [Task name]

**Task:** [One sentence describing the objective and deliverable.]

**Domain:** [Field, then 1–2 sentences explaining the central concept for a
competent CS engineer unfamiliar with it.]

**Inspected:** [Repository, task path, revision/PR, and material missing evidence.]

## Assessment

| Aspect | Judgment | Evidence / limits |
| --- | --- | --- |
| Frontier-model difficulty | [Judgment and confidence; measured or estimated] | [Task-specific results and run conditions, or bottlenecks and missing evidence] |
| Realism | [Realistic / mixed / puzzle, with a brief reason] | [Practitioner workflow and any artificial constraints] |
| Verifier | [Artifact checks / code execution / environment checks / hybrid] | [What is checked and how it is scored; key mismatch or blind spot] |
| Isolation | [Mechanisms observed, absent, or unknown] | [Execution boundary, permissions, mounts/network, limits, and source of guarantees] |

## Flow

[Mermaid or ASCII diagram with labeled requests, inputs, outputs, and visibility
boundaries.]

[Short explanation of the central operation and a concrete example if needed.]

## What the verifier proves

[Explain the checks, reference/hidden data, scoring rule, and what a passing
result does and does not establish. Cite implementation evidence.]

## Review guidelines

[Link the applicable guidance, or say none was found.]

| Criterion | Status | Evidence / shortfall |
| --- | --- | --- |
| [Applicable criterion] | [Meets / falls short / unknown / not applicable] | [Code or document reference; consequence and suggested correction if needed] |

## Read these 3–5 sections

| Code section | What it does / why it matters |
| --- | --- |
| [Linked file and line numbers] | [Task contract or key behavior] |

[End with the first applied knowledge-check question only. Wait for the reply.]
