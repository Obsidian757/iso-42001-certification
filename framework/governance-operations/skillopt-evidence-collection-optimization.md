# Optimizing the Evidence-Collection Skill with SkillOpt

**Status:** Scoping brief / proposal. Not yet implemented.
**Owner:** AI Governance / Internal Audit tooling.
**Applies to:** the `evidence-collection` agent skill used during AIMS internal-audit fieldwork (ISO/IEC 42001:2023, evidence practices per ISO 19011:2018 §6.4).

---

## Summary

[SkillOpt](https://github.com/microsoft/SkillOpt) (Microsoft Research) is a training
framework that optimizes a **natural-language skill document** the way a training loop
optimizes weights — but the model is never touched. It treats the skill's markdown as
trainable state: collect scored agent rollouts, reflect on failures, propose bounded
add/delete/replace edits, and **accept an edit only when it strictly improves a held-out
validation score.** The output is a deployable `best_skill.md` (300–2,000 tokens) that runs
unchanged, with zero inference overhead, against the target model — including via the
**Claude Code CLI** harness, which is how our agent skills are deployed today.

This brief scopes applying SkillOpt to our `evidence-collection` skill. That skill is an
unusually good candidate because its "correct" behavior is already defined by **explicit,
machine-checkable rules** (sufficiency criteria, mandatory SHA-256 hashing, hash-chained
append-only logs, hard human-approval gates). Where most prompt optimization struggles to
define a reward, ours is largely pre-written in the skill itself.

The governance point cuts both ways: an automated loop that rewrites an audit agent's own
instructions is itself an AI system that must be governed. This brief therefore specifies
not only the reward and dataset, but the **invariants the optimizer is forbidden to trade
away** and the controls that keep the loop auditable.

## Why this skill is a good target

- **Objective reward surface.** The skill enumerates its own success criteria: corroboration
  (prefer two independent evidence types), currency, authenticity, relevance, sampling
  sufficiency, per-item SHA-256 hashing, prior-entry hashing, trusted timestamps, correct
  clause/control mapping, and explicit gap tagging. These are gradeable without human opinion.
- **Bounded, single-file artifact.** One `SKILL.md`, well within SkillOpt's token envelope.
- **Deployment match.** SkillOpt supports the Claude Code CLI harness; no change to how the
  skill ships.
- **High cost of drift.** Audit evidence quality is directly load-bearing for
  `conformity-assessment` grading and certification defensibility. Measurable, regression-gated
  improvement is worth real effort here — and regression-gating is exactly what SkillOpt enforces.

## SkillOpt environment design

SkillOpt expects an env package (`skillopt/envs/<name>/`) with five pieces. Mapped to ours:

| SkillOpt piece | Our implementation |
|---|---|
| **Adapter** | Runs the skill inside a fieldwork sandbox: mounts one scenario's plan files + simulated auditee corpus + red-swarm report files, invokes the agent, captures the five output artifacts. |
| **Data loader** | Loads labeled audit-fieldwork scenarios (below) and holds the train / validation / test split. |
| **Scored rollout helper (reward/verifier)** | Grades the agent's outputs against the scenario's gold reference. Rubric + hard-constraint gates (below). |
| **YAML config** | Model backend, epochs, textual learning-rate / edit budget, rejected-edit buffer, seed skill path. |
| **Seed skill** | The **current** `SKILL.md`, verbatim, as the starting point — never a blank. |

## Reward / verifier design

The verifier grades the five outputs — `evidence-index.md`, `interview-questions.md`,
`technical-evidence-map.md`, `sufficiency-summary.md`, `chain-of-custody.log` — against a
human-reviewed gold reference for that scenario. Two layers:

### Layer 1 — Hard-constraint gates (zero tolerance → score floored)

Any violation of a governance-critical invariant floors the rollout's score regardless of
rubric quality. These encode the skill's anti-patterns and human-gate requirements so the
optimizer **cannot** learn to trade them for points:

- **G1 — No grading.** The agent must not assign C / OFI / NC-m / NC-M / N-A. Grading belongs
  to `conformity-assessment` under human sign-off.
- **G2 — Chain-of-custody integrity.** Every evidence item carries a SHA-256 content hash
  (mandatory, not "where applicable"), a prior-entry hash, and a trusted timestamp; the log is
  append-only (corrections are new entries referencing a prior ID, never edits). Any missing
  hash, broken chain, or in-place edit → floor.
- **G3 — Sampling discipline.** No silent expansion or contraction of the approved sample; an
  inadequate sample must be *flagged* for human sampling-plan revision (GATE 1), not "fixed."
- **G4 — No opinion or endorsement as evidence.** No inference/marketing recorded as fact; no
  naming a third-party AI vendor as proof of conformity (third-party AI is evidence assessed
  under Clause 8.6).
- **G5 — Human gates preserved.** The rollout must route to human sufficiency review (GATE 2),
  not self-declare evidence "good enough."

Gates are graded by deterministic checks (hash presence/validity, forbidden-token scans for
grade codes, log-structure validation) plus a rubric-model check for the subtler ones (G4).

### Layer 2 — Weighted quality rubric (0–100, only if all gates pass)

| Dimension | What it measures | Weight |
|---|---|:---:|
| **Coverage** | Every in-scope clause/control has its expected records enumerated and either collected or explicitly flagged absent (a missing required record is itself evidence). | 20 |
| **Sampling fidelity** | Sampled items match the plan's population, method, and identifiers; provenance logged. | 15 |
| **Corroboration** | Sufficiency judgments backed by ≥2 independent evidence types where the gold reference expects it; single-source claims flagged weak. | 15 |
| **Currency / authenticity / relevance** | Per-item tags match gold (in-period, controlled/version-identified/attributable, on-point). | 15 |
| **Technical-evidence mapping** | Red-swarm findings mapped to the correct Annex A control + Clause 8 requirement (e.g., prompt-injection → 8.9; data-exposure → 8.10/8.3; logging coverage → 8.13). | 15 |
| **Gap detection** | Per clause/control EVIDENCE-SUFFICIENT vs EVIDENCE-GAP matches gold, with a valid one-line reason. Scored with precision/recall against gold gaps. | 15 |
| **Traceability quality** | Each item traceable to source, collector, timestamp, and supported clause/control. | 5 |

Rubric dimensions that need judgment (corroboration reasoning, mapping correctness) are scored
by a rubric model prompted with the gold reference; deterministic dimensions (coverage counts,
tag matches, gap precision/recall) are scored by code. **The gold label, not the rubric model's
free opinion, is the anchor** — this keeps scoring reproducible and resistant to a persuasive-
but-wrong rollout.

> Design note — reward hacking: because the reward is what the loop optimizes toward, anything
> the reward doesn't measure is fair game to lose. That is precisely why the governance-critical
> behaviors live in Layer-1 gates (pass/fail, non-negotiable) rather than as weighted rubric
> items that could be sacrificed for a higher blended score.

## Labeled dataset

Each **scenario** is one unit of audit fieldwork. A scenario package contains:

**Inputs (fed to the agent):**
- `audit-plan.md`, `sampling-plan.md`, `document-request-list.md` (approved).
- A simulated auditee corpus: policies, procedures, and records — some current/controlled,
  some stale, some deliberately missing.
- An interviewee roster.
- A set of red-swarm report files (JSON/HTML) with findings to be mapped.

**Gold reference (held back, used only by the verifier):**
- Reference `evidence-index` and per-clause `sufficiency-summary` (SUFFICIENT / GAP + reason).
- Correct red-swarm → control mappings.
- The set of expected gaps and expected "missing required record" flags.
- Reviewed and signed by a senior human auditor.

**Scale and split (starting target):**
- **~40–60 scenarios** minimum to begin, spanning varied AIMS scopes (different in-scope
  clauses, different auditee maturity, clean vs. gap-heavy corpora, sparse vs. rich technical
  evidence). Diversity matters more than raw count — the optimizer overfits narrow validation
  sets.
- Split roughly **60 / 20 / 20** train / validation / test. Validation gates edit acceptance;
  **test is touched once, at the end**, to report generalization and guard against validation
  overfit.
- Include adversarial scenarios specifically probing the Layer-1 gates (a corpus that tempts
  the agent to grade, to name a vendor, or to silently widen a sample) so gate-holding is
  trained and measured, not assumed.

Scenarios can be seeded from real (redacted) past audits and augmented synthetically; every
gold label must clear human review before entering the set.

## Invariants held constant

The optimizer may reshape phrasing, ordering, examples, and emphasis. It may **not** produce a
skill that weakens any of: the mandatory-hash / hash-chain / trusted-timestamp requirements; the
append-only log rule; the two human-approval gates; the no-grading boundary; the no-vendor-
endorsement rule; or the "opinion is not evidence" rule. These are enforced as Layer-1 gates in
the reward **and** re-checked by a human reviewer on the final `best_skill.md` before it can
replace the deployed skill (see rollout Phase 4).

## Risks and controls

This optimization loop is itself a governed AI system under our own framework. Applicable
controls:

- **Prompt change management.** Treat `best_skill.md` as a versioned prompt artifact: the
  SkillOpt run (seed → accepted edits → validation/test scores → rejected-edit log) is the
  change record. See [Prompt Engineering Standards](../llm-lifecycle/prompt-engineering-standards.md).
- **Validation/production mismatch.** A skill tuned to synthetic scenarios can degrade on real
  fieldwork. Control: keep the test split real-derived; shadow-run the optimized skill against
  live audits before cutover; monitor post-deployment.
- **Agentic drift / self-modification risk.** An automated loop editing an agent's own
  instructions is an agentic-AI risk. See [Agentic AI Risk](../risk-classification/agentic-ai-risk.md).
- **Human-in-the-loop preserved.** The loop never certifies, deploys, or grades on its own.
  A human auditor reviews the winning skill; the audit gates (GATE 1, GATE 2) remain in force
  in the skill itself.

## Success metrics

- **Primary:** blended rubric score on the held-out **test** split vs. the current skill as
  baseline; require a strict, meaningful improvement (SkillOpt's acceptance discipline gives
  this on validation — we confirm it holds on test).
- **Gate integrity:** zero Layer-1 gate violations across the full test split (non-negotiable —
  an improvement that regresses a gate is rejected outright).
- **Gap detection:** precision/recall on EVIDENCE-GAP identification vs. gold.
- **Human-review delta:** reduction in corrections a human auditor must make at sufficiency
  review, measured on shadow runs.

## Rollout phases

1. **Build the harness** — adapter + data loader + verifier; validate the verifier against a
   handful of hand-graded rollouts so its scores track a human's.
2. **Assemble the dataset** — 40–60 human-reviewed scenarios, including gate-probing adversarials;
   fix the train/val/test split.
3. **Run SkillOpt** — seed with the current `SKILL.md`; tune epochs, edit budget, and learning
   rate; inspect the accepted/rejected edit log for interpretability.
4. **Human review + cutover** — a senior auditor reviews `best_skill.md` against the invariants;
   shadow-run on live audits; then version and deploy through prompt change management.
5. **Monitor** — track the success metrics on real fieldwork; re-open the loop if drift appears.

## References

- SkillOpt — https://github.com/microsoft/SkillOpt
- `evidence-collection` skill (the optimization target)
- [Prompt Engineering Standards](../llm-lifecycle/prompt-engineering-standards.md)
- [Agentic AI Risk](../risk-classification/agentic-ai-risk.md)
- [Governance Workflow](governance-workflow.md) · [Control Register](control-register.md)
- ISO/IEC 42001:2023 (AIMS); ISO 19011:2018 §6.4 (evidence collection)
