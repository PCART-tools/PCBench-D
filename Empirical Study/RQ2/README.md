RQ2 studies how deprecated APIs and candidate replacement APIs behave across version evolution. The study first constructs a controlled candidate-API scope and API migration scenarios, extracts the source code of deprecated and candidate APIs, and computes similarity and candidate rankings across versions. It then analyzes version trends in similarity/ranking, identifies key versions and their dominant causes, and further examines how candidate-related factors and code change patterns affect API migration.

RQ2 uses three similarity algorithms, named **graph-based**, **token-based**, and **tree-based** in the paper; the repository implements them as the modules `mapBased`, `tokenBased`, and `treeBased`, and keeps this identifier spelling in code, JSON keys, and output filenames. Similarly, the repository's cause directories `dep_rep`, `common_cause`, and `candidates_cause` correspond to the paper's **pair-dominant**, **mixed**, and **other-candidate-dominant** categories. The subdirectory READMEs below use the paper's names when describing these algorithms and categories.


## Directory Structure

```text
RQ2/
├── input/
├── lookup_source_def/
├── measure_similarity/
├── RQ2.1/
├── RQ2.2/
├── RQ2.3/
└── environment.yml
```

| Directory | Main contents |
| --- | --- |
| `input/` | Candidate-scope filtering results and final experimental-scenario Excel data |
| `lookup_source_def/` | Tools for extracting deprecated-API and candidate-API source code |
| `measure_similarity/` | Tools for constructing version combinations, computing similarity, and ranking candidates |
| `RQ2.1/` | Trend analysis of similarity/ranking across versions |
| `RQ2.2/` | Key-version identification, cause attribution, and candidate-API impact analysis |
| `RQ2.3/` | Analysis change-block identification and code change-pattern analysis |
| `environment.yml` | Python/Conda environment configuration |

Detailed descriptions are available in the corresponding README files:

- [input/README.md](input/README.md)
- [lookup_source_def/README.md](lookup_source_def/README.md)
- [measure_similarity/README.md](measure_similarity/README.md)
- [RQ2.1/README.md](RQ2.1/README.md)
- [RQ2.2/README.md](RQ2.2/README.md)
- [RQ2.3/README.md](RQ2.3/README.md)


## Overall Workflow

The main relationships among the RQ2 components are:

```text
input/
  │
  ├── Candidate scope and migration-scenario Excel files
  │
  ▼
lookup_source_def/
  │
  ├── Extract deprecated-API source code
  └── Extract candidate-API source code
  │
  ▼
measure_similarity/
  │
  ├── Construct query/candidate version combinations
  └── Compute similarity and generate candidate rankings
  │
  ├─────────────────────┬─────────────────────┐
  ▼                     ▼                     ▼
RQ2.1                 RQ2.2                 RQ2.3
Version trends        Key versions and      Change blocks and
                      cause analysis        change patterns
```

The components are related as follows:

- `input` provides the candidate-scope and migration-scenario information;
- `lookup_source_def` prepares the source-code data from that information;
- `measure_similarity` computes similarity and produces ranking results; and
- `RQ2.1`, `RQ2.2`, and `RQ2.3` perform different levels of analysis based on those ranking results.


## Main Functions and Outputs

The six RQ2 modules form a sequential pipeline. Their detailed input formats, processing steps, and output structures are documented in the corresponding subdirectory READMEs.

| Module | Role | Main output |
| --- | --- | --- |
| `input/` | Candidate-scope filtering and migration-scenario construction | Filtering and scenario Excel files |
| `lookup_source_def/` | Deprecated-API and candidate-API source extraction | Versioned source-code directories |
| `measure_similarity/` | Version selection, similarity computation, and candidate ranking | Similarity-ranking JSON files |
| `RQ2.1/` | Similarity/ranking trend analysis | `fix_D.xlsx`, `fix_R.xlsx` |
| `RQ2.2/` | Key-version identification and cause analysis | Phase and cause statistics |
| `RQ2.3/` | Code-change-block and change-pattern analysis | `mode_stats.xlsx` |

Candidate-scope construction yields **723 mappings**. The final experimental scenarios include:

- **D-fixed scenarios:** 529.
- **R-fixed scenarios:** 443.
- **Covered API mappings:** 557.

`measure_similarity/` also produces `fix_D_t` as an intermediate scenario. Because it overlaps with the other migration scenarios, `fix_D_t` is removed from the final experimental results; the retained final scenarios are `fix_D` and `fix_R`.


## Environment Configuration

Project dependencies are recorded in:

```text
environment.yml
```

The specific Python dependencies, input paths, and output paths required by each script are documented in the README of the corresponding subdirectory.
