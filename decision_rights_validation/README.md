# Decision Rights V2 — adversarial validation

Independent research prototype. This package supplements, rather than replaces, the earlier matched simulation and working paper.

## Reproduce (Python 3.10+, standard library)
```
python run.py --out reproduction
```
The committed 48-case benchmark has a SHA-256 manifest checked before execution. `build_benchmark.py` documents its construction; rebuilding changes the frozen benchmark only if the authored cases are edited. The test oracle was manually authored in the same development session, not by an independent evaluator. All 48 fixture cases passed, with 11 allowed, 22 blocked, 14 escalated and one rolled back; three repeated mutations were suppressed. Actual transactions are executed in isolated in-memory SQLite databases, with state and audit snapshots persisted to `fixture_run/benchmark.sqlite`. The fixture results do not measure LLM behavior or human performance.

## What changed
The trusted operation mandate now binds operation, exact record ID and exact value/type. Unknown fields fail schema validation, including claimed authorization and tier overrides. Tier-4 or salary mutations require two distinct allowlisted simulated approvers; tier-1 mutation requires one. Bounded cross-system requests escalate; delegated requests require risk, evaluation and rollback gates. Replays of committed mutation IDs are suppressed. Infrastructure stop flags apply before any action. Transaction faults roll back all changes in the same SQLite transaction.

## Limitations
Approver IDs are trusted test metadata, not authenticated signatures or actual human decisions. The prototype simulates execution after human authorization; it does not enforce human-only execution through a separate authenticated principal. Mandates themselves must be produced by trusted application code; their correctness is assumed. Exact-value matching is deliberately restrictive and not suitable for unrestricted free-text drafting. The local test audit persists even when the external audit availability flag is false. Real audit sink failures, concurrency, external API transactions, cross-tenant isolation, approval expiry/revocation, and recovery from distributed failures are not validated. The suite is a developer-authored regression suite, not a blinded or independent benchmark. Hashing makes changes detectable but is not a third-party timestamp or preregistration.

## Optional live model smoke run
Set `OPENAI_API_KEY` and `MODEL_ID` in your own secure environment (never include keys in the repository). Select an available model supporting Chat Completions JSON-object responses. The runner sends synthetic text only, makes at most 48 billable calls and records provider response IDs, model, usage and latency where returned.
```
python run.py --live --max-calls 48 --out live_smoke
```
Live proposals replace authored fixture inputs. Fixture pass rates are not computed in live mode because the oracle labels apply to the prescribed proposal, not to any model output. Several cases share similar user prompts and differ in trusted control state; this is a gateway smoke run, not a statistically valid model benchmark. API errors are recorded separately and fail closed. No live calls were executed in the supplied run because credentials were absent.

## Next experimental protocol (proposed, not executed)
1. Recruit two independent reviewers to label a new held-out set of tasks, with authorization context separated from untrusted text. Freeze a versioned dataset before running models; adjudicate label disagreements and log changes. Include ordinary tasks, ambiguous requests, wrong targets/values, injection, missing approvals, and infrastructure faults.
2. Run the same planner outputs through three matched arms: unrestricted business permissions (sandbox only), blanket human approval, and risk-tiered authorization. Share infrastructure protections and compare a mandate-only ablation. Log model IDs, prompts, raw responses, token usage, errors and observed local/API elapsed time. Do not exclude API errors from availability denominators.
3. Separate exact authorized completion, unauthorized mutation, escalation, false refusal, rollback, and human workload. Report paired differences and intervals at the task level, stratify by task type, report all adverse events. Report any human review cost and time as modeled unless actual reviewers are recruited and timed. Use a pilot to estimate paired disagreement rates and plan sample size before confirmatory analysis.
4. Only after external validation, update the working paper and publish the code/data with all synthetic and live-model results clearly labeled. Organizational productivity and employee cognitive load require real consenting teams; no sandbox can establish those effects.
