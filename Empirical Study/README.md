This directory contains the empirical study of the **evolution of deprecated APIs and their replacements in Python libraries**. It traces how a deprecated API relates to its replacement, how the pair co-evolves across versions, and what happens after the deprecated API is announced as deprecated.

> Full checkout and reproduction of this artifact require Linux. Windows is not supported because some repository paths differ only by letter case. See the [Platform Support](../README.md#platform-support) section in the repository root README for details.

The study is organized into one data-collection stage and three research questions:

```text
Empirical Study/
├── Data Collection/   # builds the shared dataset
├── RQ1/               # replacement locality and interface differences
├── RQ2/               # similarity/ranking evolution, key versions, change patterns
└── RQ3/               # API lifecycle after deprecation
```


## Overview

The study traces the evolution of deprecated APIs and their replacements from a common dataset of **830 deprecated-API → replacement-API mappings** collected from **33 popular Python libraries**. Three research questions follow this evolution:

- **RQ1** characterizes the deprecated-to-replacement relationship itself: where the replacement is located relative to the deprecated API, and how their parameter interfaces differ.
- **RQ2** studies how the pair evolves across versions: how similarity and candidate ranking change, which key versions mark the transition, and which code changes drive those shifts.
- **RQ3** studies the end of the lifecycle: what happens after a deprecation announcement, distinguishing cases where the original invocation fails before source-definition removal from cases where source-definition removal happens first.


## Directory Structure

| Directory | Contents |
| --- | --- |
| `Data Collection/` | Constructs the deprecated-to-replacement mapping dataset used by all three RQs |
| `RQ1/` | Replacement locality and parameter-interface differences |
| `RQ2/` | Similarity/ranking trends, key versions, and code change patterns |
| `RQ3/` | Lifecycle analysis after deprecation |

Detailed descriptions are provided in the corresponding README files:

- [Data Collection/README.md](Data%20Collection/README.md)
- [RQ1/README.md](RQ1/README.md)
- [RQ2/README.md](RQ2/README.md)
- [RQ3/README.md](RQ3/README.md)


## Data Collection

The Data Collection stage produces the shared dataset from the changelogs of `33` Python libraries. It includes a pilot study for changelog retrieval, formal collection of deprecation entries, source-definition verification, and invocation-case generation.

The result is `final_dataset.xlsx` — `830` mappings (`207` classes, `239` functions, and `384` methods), each carrying the deprecation-announcement version and the observed source-definition removal and original-invocation failure status — together with executable invocation cases used to verify invocation status across releases. Ending events not observed by the lifecycle cutoff are marked in the dataset.


## RQ1: Replacement Locality and Interface Differences

RQ1 characterizes the deprecated-to-replacement relationship to inform candidate search and migration adaptation:

- **RQ1.1 Replacement Locality** classifies where replacements are located relative to deprecated APIs (module paths, names, and enclosing classes).
- **RQ1.2 Parameter-Interface Differences** compares parameter lists of deprecated and replacement APIs, using PCART to classify their differences.


## RQ2: Evolution, Key Versions, and Change Patterns

RQ2 studies how a deprecated API's relationship to candidate replacements changes across versions:

- **RQ2.1** analyzes similarity/ranking trends across versions.
- **RQ2.2** identifies key versions, attributes their dominant causes, and analyzes candidate-API impact.
- **RQ2.3** identifies analysis change blocks and summarizes code change patterns.

RQ2 relies on source extraction (`lookup_source_def`) and similarity computation (`measure_similarity`) before its three sub-analyses.


## RQ3: API Lifecycle After Deprecation

RQ3 studies what happens after a deprecation announcement by comparing the source-definition removal version with the original-invocation failure version. It distinguishes:

- **invocation-first**: Invocation fails while the source definition still exists.
- **source-first**: The source definition is removed first, but the API remains callable through aliases, inheritance, dynamic resolution, or other mechanisms.

The analysis identifies the causes and proportions of each behavior.


## Third-Party Software

Some analyses rely on third-party research tools.

In particular, **PCART** is used as an external tool for the parameter-interface analysis in RQ1.2. PCART is not redistributed as part of this repository and remains subject to its own **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See the official [PCART repository](https://github.com/PCART-tools/PCART) for its source code and license information.
