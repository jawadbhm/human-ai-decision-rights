# Decision Rights in Human–AI Organizations

**Current official release:** Version 0.5 · November 28, 2026  
**Version DOI:** [10.5281/zenodo.24628610](https://doi.org/10.5281/zenodo.24628610)  
**Concept DOI:** [10.5281/zenodo.24584260](https://doi.org/10.5281/zenodo.24584260) · resolves to the latest version  
**Public record:** [https://zenodo.org/records/24628610](https://zenodo.org/records/24628610)  
**Previous version:** [Version 0.2](https://zenodo.org/records/24584261)  
**Research website:** [https://human-ai-decision-rights.vercel.app](https://human-ai-decision-rights.vercel.app)

Version 0.5 is the author-approved public release. The LaTeX-formatted PDF and source are in the paper directory. The complete release and replication package is in replication/Decision_Rights_v0_5_Publication_Kit.zip; the separately downloadable live-pilot software kit is also in replication/. The repository's v0.2 paper remains in the paper directory as historical material and is not the current release.

## Abstract

As AI agents acquire execution capabilities, organizations face the problem of delegating routine actions while preserving accountability and limiting review costs. This paper develops a four-tier decision-rights model and examines its operation in a synthetic business-workflow sandbox. A matched simulation of 1,000 cases compares unrestricted decision rights, blanket review of mutations, and risk-tiered governance combined with a trusted operation mandate. Under the default assumptions, the combined configuration produces zero trials with unauthorized persistent mutations, compared with 268 and 5 in the alternatives; the corresponding counts of changed records are 0, 376 and 7. It routes 341 cases to review, compared with 785 under blanket review. A post-hoc ablation yields 6 affected trials for tier rules alone and 190 for the mandate alone. Sensitivity analysis identifies residual vulnerabilities under modeled reviewer error. A reduced-form loss model derives the accuracy threshold below which discretionary review is economically preferable. A separate four-arm gateway smoke test evaluates 20 existing fixtures (80 policy evaluations) and passes 13 software unit tests. The test isolates mandate enforcement from review routing in the implementation. These results concern synthetic workflows and software behavior; live model performance and actual human review remain unmeasured.

## Research status and limits

The Version 0.5 manuscript reports a matched synthetic simulation and software checks. The main comparison uses 1,000 synthetic cases per arm. Its separate four-arm gateway smoke test evaluates 20 existing fixtures (80 policy evaluations); 13 software unit tests passed. These are simulation and software results, not measured human performance or independent empirical validation. No live LLM experiment or human-participant study has been completed. Both remain prospective. The publication does not claim that these studies were executed.

## Repository contents and reproduction

- paper/Decision_Rights_in_Human_AI_Organizations_v0_5.pdf — current manuscript.
- paper/Decision_Rights_in_Human_AI_Organizations_v0_5.tex — LaTeX source used for the current layout.
- paper/Decision_Rights_in_Human_AI_Organizations_v0_2.pdf — preserved previous-version file.
- replication/Decision_Rights_v0_5_Publication_Kit.zip — complete release package, including the PDF, LaTeX source, research materials and integrity manifest.
- replication/Decision_Rights_Live_Pilot_Engineering_Kit.zip — software evaluation code, fixtures, outputs, tests and prospective protocol.
- Existing Python source, synthetic datasets, recorded outputs and analysis documentation remain in the repository.

For the main matched simulation and frozen validation suite, from the repository root:

~~~sh
python3 governance_comparative/experiment.py --out reproduction/main
python3 decision_rights_validation/run.py --out reproduction/v2
python3 verify.py reproduction/main/summary.json reproduction/v2/summary.json
~~~

The commands reproduce the archived summary metrics and fixture outcomes under the documented assumptions. They do not run live models or recruit human participants. The pilot kit contains its own README, software tests and checksums. SHA256SUMS.txt covers the repository's tracked release files; the publication kit has its own manifest.

## Citation

Bahoum, Jawad (2026). *Decision Rights in Human–AI Organizations: A matched simulation of agent autonomy, human accountability, and review workload* (Version 0.5). Zenodo. https://doi.org/10.5281/zenodo.24628610

Use the version-specific DOI for this manuscript. The concept DOI 10.5281/zenodo.24584260 resolves to the latest version; prior publication versions remain in Zenodo's version history and through their version DOIs.

## Licensing and disclosures

- Version 0.5 manuscript PDF and LaTeX source: **CC BY 4.0** — see LICENSE-PAPER.md.
- Original research software: **MIT** — see LICENSE-CODE.txt.
- Original synthetic datasets: **CC0 1.0** — see LICENSE-DATA.txt.

These are separate scopes; the record-level manuscript license does not replace software or dataset notices. This research received no external funding. The author declares no competing interests. AI assistance supported prototype development, fixture design, computational checks and manuscript preparation; the author is responsible for the research and its interpretation. Third-party cited material and trademarks are excluded from these author-held licenses.
