# friction

Make annoying work disappear.

The `solve` skill treats time and attention as scarce resources. It looks past
the default do-it-yourself answer and finds a practical way to finish the job:
do it directly, automate it, or hire the right specialist, concierge, courier,
assistant, or local service. It then carries the solution through as far as the
user's authority allows.

This is inspired by Jeffrey Lind's
[Billionairebot](https://grokbot.dev/marketplace/billionairebot/), which reframes
dreaded chores by asking how someone with abundant resources would offload
them. `friction` extends that idea from recommendations to verified execution,
while keeping spending and external actions inside explicit boundaries.

See the [main installation guide](../../README.md#installation) for Claude Code,
Codex, and standalone Agent Skills setup.

## Skills

<!-- BEGIN GENERATED SKILLS -->
- [`solve`](skills/solve/SKILL.md) — Eliminate real-world friction end to end through direct action, paid delegation, specialist services, or automation. Use when the user wants an annoying chore, errand, logistical problem, or recurring burden handled rather than merely explained.
<!-- END GENERATED SKILLS -->

## Standing authorizations

The skill reads `AUTHORIZATIONS.md` from the working directory when the file is
present. Use it to record actions the agent may take without stopping for a
second approval. The current request still counts as task-specific authority;
the file is for reusable boundaries.

Example:

```markdown
# Standing authorizations

- Appointments: You may book, reschedule, and cancel routine personal
  appointments for me. Prefer weekdays from 9:00 a.m. to 5:00 p.m. Add confirmed
  appointments to my calendar. Do not consent to treatment, sign waivers, or
  accept a cancellation fee above the spending limit below.
- Reversible actions: You may make changes in my own accounts, files, and
  settings when they are fully reversible at no cost. This does not include
  deleting data, contacting people, publishing content, changing security or
  privacy settings, or cancelling a paid service.
- Spending: You may spend up to $75 total per task, including taxes, fees, tips,
  and shipping. Do not start subscriptions, accept recurring charges, buy gift
  cards, or split a purchase to stay under the limit.
- Providers: You may contact businesses to request quotes, availability, and
  service details. Do not contact my employer, family, friends, or medical
  providers unless another authorization explicitly allows it.
```

Write boundaries that are specific enough to audit. If the file is absent or a
needed action is outside its limits, the skill prepares everything it safely can
and asks for the smallest missing approval at the final boundary.
