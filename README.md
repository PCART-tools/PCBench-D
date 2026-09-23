# PCBench-D

PCBench-D is a benchmark and replication package for studying how deprecated APIs and their replacements evolve across versions of Python libraries. It contains **830 maintainer-specified deprecated API → replacement API mappings** from **33 libraries**, **830 manually reviewed invocation cases**, and the data and scripts for an empirical study of replacement locality, cross-version rankings, and post-deprecation lifecycles.

The related [PCBench](https://github.com/PCART-tools/PCBench) benchmark focuses on Python API parameter compatibility. PCBench-D uses the same set of 33 libraries but studies deprecated API–replacement API relationships and the continued availability of deprecated APIs.


## Contents

| Component | What it provides |
| --- | --- |
| [`Benchmark/`](Benchmark/README.md) | The mapping table, changelog and source evidence, lifecycle-event records, and executable invocation cases |
| [`Empirical Study/`](Empirical%20Study/README.md) | Data-collection artifacts, analysis scripts, and results for RQ1–RQ3 |

The benchmark records when deprecation is announced and, when observed by the lifecycle cutoff, when the original source definition is removed and when the original invocation fails. These last two events can occur in either order. The [benchmark documentation](Benchmark/README.md) describes the dataset schema, value conventions, and invocation cases.


## Platform Support

This repository is supported for full checkout and reproduction on Linux.

Windows is not supported because the repository contains paths that differ only by letter case. On the default Windows filesystem, these paths may be treated as the same path, causing checkout conflicts and inaccurate `git status` results. Enabling Git's `core.longpaths` option does not resolve this issue.

For full reproduction, use a case-sensitive Linux filesystem. When using WSL2, keep the repository in the Linux filesystem rather than under a Windows-mounted directory.


## Repository Layout

```text
├── Benchmark/
│   ├── deprecated_api_replacement_api_mappings.xlsx
│   ├── invocation_cases/
│   └── README.md
├── Empirical Study/
│   ├── Data Collection/
│   ├── RQ1/
│   ├── RQ2/
│   ├── RQ3/
│   └── README.md
├── LICENSE-CODE
├── LICENSE-DATA
└── README.md
```

The empirical-study artifacts are organized by data collection and three research questions: RQ1 (replacement locality and parameter interfaces), RQ2 (cross-version rankings and code changes), and RQ3 (post-deprecation lifecycle). Some steps require environment-specific setup or manual verification; the [empirical-study documentation](Empirical%20Study/README.md) identifies the available inputs, outputs, and procedures.


## Getting Started

To inspect the curated mappings and lifecycle records, open [`Benchmark/deprecated_api_replacement_api_mappings.xlsx`](Benchmark/deprecated_api_replacement_api_mappings.xlsx). The [Benchmark README](Benchmark/README.md) explains its columns and the organization of the invocation cases.

To run one invocation case from the repository root on Linux:

```shell
cd Benchmark/invocation_cases/numpy/numpy.core.arrayprint.ComplexFormat@1.13.3
conda env create -f environment.yml
conda activate numpy_1.13.3
python numpy.core.arrayprint.ComplexFormat.py
```

This runs the case in its starting environment; identifying the first failure requires testing the invocation across subsequent library releases. See the [Benchmark README](Benchmark/README.md) for the lifecycle-testing procedure and cases needing external adaptation.

To inspect the study's existing inputs and results, start with [`Empirical Study/Data Collection/final_dataset.xlsx`](Empirical%20Study/Data%20Collection/final_dataset.xlsx) and the [RQ1](Empirical%20Study/RQ1/README.md), [RQ2](Empirical%20Study/RQ2/README.md), and [RQ3](Empirical%20Study/RQ3/README.md) directories. To rerun an analysis, follow the dependencies, commands, and expected outputs in the [Empirical Study README](Empirical%20Study/README.md) and the relevant subdirectory README.


## Third-Party Software

Some parts of the empirical study rely on third-party research tools.

In particular, **PCART** is used as an external tool in the empirical study. PCART is licensed separately under the **GNU Affero General Public License v3.0 (AGPL-3.0)** and is not covered by the licenses applied to the original data and source code in this repository.

PCART is not redistributed as part of this repository. For information about PCART and its license, see the official [PCART repository](https://github.com/PCART-tools/PCART).

Other third-party software, source code, changelog excerpts, and referenced materials remain subject to their respective copyright and license terms.


## License

This repository contains both research data and source code, which are licensed separately.

- The benchmark data, curated annotations, and other original research data are licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0) License**. See [`LICENSE-DATA`](LICENSE-DATA).
- The invocation cases, empirical-analysis scripts, and other original source code are licensed under the **MIT License**. See [`LICENSE-CODE`](LICENSE-CODE).

Third-party materials are not relicensed by this repository and remain subject to their respective licenses and copyright terms.
