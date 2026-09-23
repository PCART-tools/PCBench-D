This directory provides a benchmark dataset for **API deprecation and migration research in Python third-party libraries**, containing **830 deprecated API → replacement API mappings** extracted and verified from the changelogs of **33 Python third-party libraries**.

Unlike datasets that only record deprecation announcements, this benchmark combines **changelog evidence, source definitions, version-evolution information, and executable invocation tests**. It captures how deprecated APIs evolve after deprecation at both the source-code and runtime levels.

> Full checkout and reproduction of this artifact require Linux. Windows is not supported because some repository paths differ only by letter case. See the [Platform Support](../README.md#platform-support) section in the repository root README for details.

The benchmark contains:

- **830 deprecated API → replacement API mappings**
- **33 Python third-party libraries**
- **207 classes, 239 functions, and 384 methods**
- **830 invocation test cases that were manually reviewed and validated across versions**

These data can support research on API deprecation, API evolution, replacement-API recommendation, cross-version compatibility analysis, and API migration.


## Directory Structure

```text
Benchmark/
├── README.md
├── deprecated_api_replacement_api_mappings.xlsx
└── invocation_cases/
```

The benchmark contains two main parts:

- **`deprecated_api_replacement_api_mappings.xlsx`**: The main data table of deprecated and replacement APIs, containing `830` mappings stored in separate worksheets by Python library.
- **`invocation_cases/`**: Executable invocation cases corresponding to the mappings in the main table. They verify the callable status of deprecated APIs across versions and identify the first failure version when one is observed by the lifecycle cutoff.


## Dataset Description

### API Mapping Table

Each record in `deprecated_api_replacement_api_mappings.xlsx` corresponds to a pair:

```text
Deprecated API → Replacement API
```

The mappings are distributed across API granularities as follows:

| Granularity | Number |
| --- | ---: |
| Class | 207 |
| Function | 239 |
| Method | 384 |
| **Total** | **830** |

Each record contains the following fields:

| Field | Description |
| --- | --- |
| `documented_deprecation_version` | Deprecation-announcement version: the version at which the changelog records the API as formally deprecated |
| `original_deprecation_log` | The original changelog entry containing the deprecated and replacement API information |
| `deprecated_api_fqn` | Fully Qualified Name (FQN) of the deprecated API |
| `replacement_api_fqn` | Fully Qualified Name (FQN) of the replacement API |
| `granularity` | API granularity: `class`, `function`, or `method` |
| `last_version_before_removal` | Release before source-definition removal: the last version in which the deprecated API's source definition still exists |
| `removal_version` | First release without the original source definition; blank if removal was not observed by the lifecycle cutoff |
| `actual_invalid_version` | First release in which the original invocation fails; `end` if failure was not observed by the lifecycle cutoff |
| `deprecated_api_source_link` | Source-definition link of the deprecated API |
| `replacement_api_source_link` | Source-definition link of the replacement API |

Together, these fields capture three aspects of a deprecated API's evolution:

```text
                           ┌─ Source-definition removal
Deprecation announcement ──┤
                           └─ Original-invocation failure
```

The relative order of **source-definition removal** and **original-invocation failure** is not fixed.

An API may remain callable after its original source definition is removed because of aliases, re-exports, inheritance, compatibility layers, or other resolution mechanisms. Conversely, its original access path or invocation form may become invalid while the source definition still exists.

The benchmark therefore records:

- the deprecation-announcement version at the documentation level;
- the source-definition removal version at the source level; and
- the original-invocation failure version at the runtime level.


## Invocation Cases

`invocation_cases/` provides executable invocation cases corresponding to the mapping records.

The directory is organized by library and API FQN:

```text
invocation_cases/
└── <library>/
    └── <FQN>@<version>/
        ├── environment.yml
        └── <FQN>.py
```

For example:

```text
invocation_cases/
└── numpy/
    └── numpy.core.arrayprint.ComplexFormat@1.13.3/
        ├── environment.yml
        └── numpy.core.arrayprint.ComplexFormat.py
```

- **`<FQN>`**: The Fully Qualified Name of the deprecated API.
- **`@<version>`**: The starting test version of the invocation case.
- **`environment.yml`**: The runtime environment used to reproduce the case.
- **`<FQN>.py`**: The test code that invokes the target API.

### What does the version in the directory name mean?

The version number in the directory name is neither the API's failure version nor the only version supported by the case. It represents:

> **The last version before the deprecation announcement (or the last version before removal if the definition was already removed), i.e., the starting point of the API's lifecycle testing.**

For example:

```text
numpy.core.arrayprint.ComplexFormat@1.13.3
```

means that invocation testing for `numpy.core.arrayprint.ComplexFormat` starts from version `1.13.3`.

During benchmark construction, subsequent versions are tested from this starting point. The invocation case is reviewed and adjusted to ensure that failures unrelated to the target API—such as missing arguments, unavailable test data, or dependency-configuration problems—do not determine the observed failure boundary.

This process identifies:

```text
Last successful invocation
        ↓
actual_invalid_version
```

where `actual_invalid_version` is the first observed version in which the API can no longer be successfully executed through its original invocation form. If no failure is observed by the cutoff, the field contains `end`.

This version-by-version execution enables the benchmark to distinguish two types of lifecycle behavior:

- **invocation-first**: The original invocation fails while the source definition still exists.
- **source-first**: The source definition is removed while the original invocation path remains functional.


## How to Run an Invocation Case

Each case provides a Conda environment configuration.

For example:

```bash
cd invocation_cases/numpy/numpy.core.arrayprint.ComplexFormat@1.13.3
conda env create -f environment.yml
conda activate <environment-name>
python numpy.core.arrayprint.ComplexFormat.py
```

To analyze an API's lifecycle, the same invocation logic can be executed under consecutive library versions to identify the point at which the original invocation first fails.

The objective is not merely to determine whether an API works in a single version, but to identify the transition:

```text
Successful invocation
        ...
Successful invocation
        ↓
First failed invocation
```

This transition determines the API's original-invocation failure boundary.


## Cases Requiring External Adaptation

Most invocation cases run directly with their provided `environment.yml` (see [How to Run an Invocation Case](#how-to-run-an-invocation-case)). A small number of cases additionally depend on conditions not captured by the Conda environment and require manual adaptation before they can be reproduced:

| Library | Case | Adaptation required |
| --- | --- | --- |
| `httpx` | `Client.send_single_request`, `Client.send_handling_redirects`, `Client.send_handling_auth`, `AsyncClient.send_single_request`, `AsyncClient.send_handling_redirects` (5 cases) | These cases issue real requests to `https://httpbin.org`. If `httpbin.org` is unreachable, replace the request URL with a reachable endpoint (e.g. a local HTTP server). |
| `polars` | `polars.io.read_sql` | The case declares a `connection_uri` of `postgresql://user:pwd@localhost:5432/db`. It stubs the `connectorx` backend (`_install_fake_connectorx`) so that `pl.read_sql` returns synthetic data without a real database; to run against a real PostgreSQL instance, change the `connection_uri` to point to your local database. |
| `sklearn` | `sklearn.datasets.lfw.load_lfw_pairs` | The `data_home` argument contains an absolute path from the original machine (`/media/he/Rbench/...`), and `load_lfw_pairs` may download the LFW dataset when it is absent. Point `data_home` to a local directory and place the LFW data there, or allow the download. |


## Dataset Construction

The benchmark was constructed through the following steps.

### Deprecation–Replacement Mapping Extraction

API deprecation records were identified from the official changelogs of `33` Python third-party libraries.

Only records for which the following relationship could be clearly determined from the changelog were retained:

```text
Deprecated API → Replacement API
```

That is, the deprecation information had to identify both the deprecated API and its suggested replacement API.

### Source-Level Verification

Candidate mappings were manually verified at the source level, including:

- confirming the actual definitions of the deprecated and replacement APIs;
- determining API granularity;
- confirming API definition locations;
- collecting corresponding source links;
- tracing the evolution of deprecated API definitions across versions; and
- determining the first version in which the source definition was removed.

### Manual Review and Cross-Version Execution

All invocation cases underwent manual review and correction before being executed across the relevant library versions. This process verified that:

1. the case actually invokes the target deprecated API;
2. it executes successfully in versions where the original invocation remains valid;
3. it does not fail because of missing parameters, test data, dependency configuration, or other unrelated errors;
4. when the invocation fails, the failure is attributable to the evolution of the target API; and
5. the API's first original-invocation failure version can be identified.

Therefore, `actual_invalid_version` is determined through **runtime execution**, rather than inferred solely from source-code differences or changelog records.

### Environment Preservation

A corresponding `environment.yml` is provided for each invocation case to specify the software environment and dependency configuration used for reproduction.


## Potential Applications

This benchmark can support studies on API evolution and software maintenance.

### API Replacement Analysis

The mappings can be used to analyze relationships between deprecated and replacement APIs, including:

- package or module location changes;
- API granularity changes;
- parameter-interface differences; and
- API structural migration patterns.

### Replacement API Recommendation

The benchmark can support the development or evaluation of replacement-API recommendation techniques, including analyses of:

- code or semantic similarity between deprecated APIs and candidate APIs;
- candidate ranking of replacement APIs;
- changes in recommendation results across library versions; and
- the influence of API evolution on replacement recommendation.

### API Lifecycle Analysis

The lifecycle fields and invocation cases support analysis of API behavior after deprecation, including:

- the interval from deprecation announcement to original-invocation failure;
- the interval from deprecation announcement to source-definition removal;
- differences between original-invocation failure and source-definition removal versions; and
- invocation-first and source-first evolution behaviors and their underlying mechanisms.

### API Migration and Compatibility Analysis

The executable invocation cases can also serve as:

- test inputs for deprecated-API detection;
- API breakage reproduction cases;
- evaluation cases for API migration techniques;
- evaluation cases for compatibility-repair techniques; and
- replacement-API validation cases.


## Reproducibility

The benchmark is designed not only to provide static deprecated-to-replacement API mappings, but also to preserve the evidence underlying the mappings and lifecycle information:

```text
Changelog evidence
        +
Source definitions
        +
Version information
        +
Executable invocation cases
        +
Reproducible environments
```

Researchers can therefore either directly analyze the curated mappings and version fields or independently examine the underlying changelog evidence, source links, and invocation cases.
