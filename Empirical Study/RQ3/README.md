RQ3 studies the lifecycle of APIs after a deprecation announcement, focusing on the time relationship and observable behavior between the API's deprecation announcement, eventual original-invocation failure, and source-definition removal.

The version points (`Va`, `Vd`, `Vi`) used here are produced by the data-collection stage (see `Empirical Study/Data Collection/README.md`); RQ3 uses them to identify and explain the lifecycle cases:

- cases are classified by the order of the observed source-definition removal (`Vd`) and original-invocation failure (`Vi`) events; the comparison also allows one or both ending events to remain unobserved at the lifecycle cutoff;
- the source code and runtime behavior of each case are then manually examined to confirm and record the specific cause.


## Research Subjects and Classification

RQ3 uses the following version points to describe the API lifecycle. They correspond to the paper's three lifecycle events — deprecation announcement (`D`), source-definition removal (`S`), and original-invocation failure (`F`):

| Field | Meaning |
| --- | --- |
| `Va` | Deprecation-announcement version (`D`); collected manually |
| `Vd-1` | Release before source-definition removal (`S-1`) |
| `Vd` | Source-definition removal version (`S`); collected manually |
| `Vi` | Original-invocation failure version (`F`); produced in the data-collection stage |

The ending events may occur in the same release, occur in different releases, or both remain unobserved by the lifecycle cutoff. The two different-release categories are:

- **Invocation-first:** The original invocation fails while the source definition still exists. If removal is later observed, `Vi` is earlier than `Vd`.
- **Source-first:** The source definition is removed while the original invocation still succeeds, for example through aliases, inheritance, or dynamic resolution. If failure is later observed, `Vd` is earlier than `Vi`.

The second ending event may remain unobserved in either category. Same-release cases and cases with neither ending event observed are included in the overall lifecycle counts but are not stored in the two cause-analysis directories below.

`Vd-1` denotes the control version before source-definition removal and helps confirm that the source definition still existed before removal.


## Input Data

RQ3 data are divided into two directories according to the order in which invocation fails:

```text
RQ3/
├── invocation-first/
│   ├── class.xlsx
│   ├── function.xlsx
│   └── method.xlsx
└── source-first/
    ├── class.xlsx
    ├── function.xlsx
    └── method.xlsx
```

Each Excel file corresponds to one API granularity:

- `class.xlsx`: Class-level APIs.
- `function.xlsx`: Function-level APIs.
- `method.xlsx`: Method-level APIs.

Each workbook contains worksheets for individual libraries and a `summary` worksheet. The main columns in the data worksheets are:

```text
D_FQN | D_url | D_type | Va | Vd-1 | Vd | Vi | reason
```

- **`D_FQN`**: Fully qualified name of the deprecated API.
- **`D_url`**: Link to the deprecated API source definition.
- **`D_type`**: API granularity.
- **`Va`**: Deprecation-announcement version.
- **`Vd-1` / `Vd`**: Versions before and at source-definition removal.
- **`Vi`**: Original-invocation failure version.
- **`reason`**: Manually verified reason or code evidence.


## Research Data Overview

### Invocation-First

The `invocation-first` group contains **43 cases**. Detailed granularity statistics, cause distributions, and cause descriptions are provided in [invocation-first/README.md](invocation-first/README.md).

### Source-First

The `source-first` group contains **147 cases**. Detailed granularity statistics, cause distributions, and cause descriptions are provided in [source-first/README.md](source-first/README.md).


## Script

[count_transition_periods.py](count_transition_periods.py) counts the APIs that go through a transition period — those whose source-definition removal version or original-invocation failure version differs from the deprecation-announcement version. It:

- reads `final_dataset.xlsx`, which is the dataset produced in the data-collection stage and located at `Empirical Study/Data Collection/final_dataset.xlsx`; RQ3 does not keep its own copy, so place a copy of that file in this directory before running;
- normalizes version strings by stripping trailing `.0` suffixes so that log-recorded versions and PyPI-style versions are comparable;
- compares `documented_deprecation_version` with `removal_version` (source-definition transition) and with `actual_invalid_version` (original-invocation transition), counting the rows in which the two values differ, broken down by `granularity` (class / function / method);
- subtracts the confirmed cases whose version records precede the deprecation announcement from the corresponding transition counts: `21` source-definition removal-version cases (class 1, function 3, method 17) from the source-definition transition count, and `17` original-invocation failure-version cases (method 17) from the original-invocation transition count;
- prints the two transition-period counts, both overall and by granularity.


## Subdirectory Descriptions

- [invocation-first/README.md](invocation-first/README.md): Statistics and cause descriptions for invocation-first cases.
- [source-first/README.md](source-first/README.md): Statistics and cause descriptions for source-first cases.
