# Decision Rights in Human–AI Organizations

**A matched simulation of agent autonomy, human accountability, and review workload**  
Jawad Bahoum · Independent research project · Working paper v0.2 · November 27, 2026

[Research website](https://human-ai-decision-rights.vercel.app) · [Final working paper](paper/Decision_Rights_in_Human_AI_Organizations_v0_2.pdf) · [Offline results explorer](docs/index.html)

This repository contains the corrected v0.2 working paper, source code, synthetic cases and datasets, recorded results, citation metadata, and instructions to reproduce the simulations. The work is an independent computational working paper and has not been peer reviewed. No DOI has been assigned.

## Abstract

As AI agents acquire execution capabilities, organizations face a design problem: how to delegate routine actions without diffusing accountability or imposing unnecessary review. This paper proposes a four-tier decision-rights model and examines its operational logic in a synthetic business-workflow sandbox. Using 1,000 matched cases, it compares unrestricted decision rights, blanket human review of mutations, and risk-tiered governance combined with a trusted operation mandate. In the default simulation, the combined configuration has 0 trials with unauthorized persistent mutations, versus 268 and 5 in the alternatives, and routes 341 cases to review rather than 785 under blanket review. The corresponding numbers of unauthorized changed database records are 0, 376 and 7, respectively. A post-hoc ablation records 6 affected trials for tier rules alone and 190 for the mandate alone. Sensitivity tests reveal residual vulnerabilities under modeled reviewer error. These are executable policy comparisons conditional on investigator-designed cases, trusted mandates and oracle-based simulated reviews. They do not establish live-model safety, actual human performance, workplace productivity or enterprise readiness.

## Main results

The default experiment applies the same 1,000 seeded synthetic tasks to three governance arms, for 3,000 matched trials. Arm C combines a four-tier policy with a trusted per-task operation mandate.

| Measure | A · Unrestricted | B · Blanket review | C · Tiered + mandate |
| --- | ---: | ---: | ---: |
| Trials with unauthorized persistent mutations | 268 (26.8%) | 5 (0.5%) | 0 (0.0%) |
| Unauthorized changed database records | 376 | 7 | 0 |
| Correct outcomes | 71.7% | 89.7% | 91.8% |
| Cases routed to simulated human review | 0 | 785 | 341 |
| Modeled total cost | $2.00 | $1,483.15 | $629.12 |
| Modeled mean latency per case | 2.0 s | 135.3 s | 58.4 s |

Costs and latency are model outputs based on stated assumptions, not observed costs or end-to-end times. The post-hoc ablation records 6 affected trials for tier rules alone and 190 for the mandate alone, so the main comparison does not isolate the effect of the tier structure. Sensitivity settings reuse the same task set and are not independent samples.

The separate V2 gateway suite contains 48 developer-authored regression fixtures; all 48 pass in the recorded run. It is not a blinded benchmark, independent validation, live-model evaluation, or evidence of production security. No external model calls or real human reviews were used in the supplied results.

## Method and limitations

The comparative experiment uses investigator-designed synthetic cases, a seeded synthetic proposal-error process, fixed sandbox operations, and a simulated reviewer whose assumed error rate is set in code. Arm C combines tier-specific routing with an operation mandate, while A and B do not use that mandate. The reviewer sees fixture-defined legitimacy and operation information; approvals are simulated rather than authenticated human decisions.

The experiments measure executable policy behavior and SQLite state changes under those assumptions. They do not test live-model safety, actual human performance, employee outcomes, productivity, or enterprise readiness. The prototype does not provide a separate authenticated human execution principal; multi-tenant isolation, distributed transactions, concurrent writes, approval expiry, real audit-sink failures, and organizational deployment remain unvalidated. The V2 suite is a developer-authored regression suite, not independent validation. See the paper and module documentation for full definitions and limitations.

## Repository map

- `paper/` — corrected v0.2 working paper PDF.
- `governance_comparative/` — matched simulation, recorded main-run cases/proposals/results, sensitivity analysis, and mock/live runner.
- `decision_rights_research/` — post-hoc control ablation.
- `decision_rights_validation/` — V2 policy gateway and frozen 48-case regression benchmark.
- `data/` — recorded ablation, sensitivity, and V2 result summaries.
- `docs/index.html` — self-contained browser explorer of the recorded results.
- `metadata/` and `CITATION.cff` — citation and archival metadata; DOI remains pending.
- `governance_comparative/README.md`, `decision_rights_validation/README.md`, and `MEASUREMENT_NOTE.md` — detailed research and measurement documentation.

The hosted research website is a separate browser-side teaching demonstration; it is not the Python execution engine used for the experiments.

## Reproduce the recorded experiments

Requirements: Python 3.10 or later. The offline reproduction commands use only the Python standard library. Run these commands from the repository root:

```sh
python3 governance_comparative/experiment.py --out reproduction/main
python3 decision_rights_validation/run.py --out reproduction/v2
python3 verify.py reproduction/main/summary.json reproduction/v2/summary.json
```

The verifier checks the reproduced main-run metrics against the committed summary and checks the V2 suite against its recorded summary. Repeated runs reproduce outcome counts; local timing can vary. Generated files go under `reproduction/`, which is ignored by Git.

Optional analyses and mock runner instructions are documented in the corresponding module READMEs. Live-model modes are optional, require credentials supplied securely by the operator, may incur provider charges, and are not needed to reproduce the supplied results. The repository contains no credentials. Never use real employee records with this prototype.

## Citation

Use the versioned paper citation in [`CITATION.cff`](CITATION.cff):

> Bahoum, Jawad (2026). *Decision Rights in Human–AI Organizations: A Matched Simulation of Agent Autonomy, Human Accountability, and Review Workload*. Independent working paper, version 0.2.

There is no DOI yet. The paper's publication and independent validation status are described in [`metadata/deposit_metadata.json`](metadata/deposit_metadata.json).

## Author and licenses

**Jawad Bahoum** is an independent researcher. The paper discloses substantial AI assistance in prototype development, fixture design, computational checks, and manuscript drafting/revision. No external funding or competing interests are declared. The project is not affiliated with or commissioned by OpenAI.

The approved licenses have separate scopes; this is not a single-license repository:

- Working paper and original manuscript text: [CC BY 4.0](LICENSE-PAPER.md).
- Source code and associated research software: [MIT](LICENSE-CODE.txt).
- Original synthetic benchmark and experiment datasets: [CC0 1.0](LICENSE-DATA.txt).

See [`LICENSES.md`](LICENSES.md) for scope and exclusions.
