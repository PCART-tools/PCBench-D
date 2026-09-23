RQ2 input data are stored in this directory and serve two purposes:

1. constructing API migration scenarios after constraining the candidate-API scope;
2. providing Excel data for subsequent source extraction, similarity computation, and trend analysis.

## 1. Candidate Scope and Migration Scenarios

The candidate-API scope follows the research design of RQ1. A mapping is retained only when its replacement lies within the parent subpackage of the deprecated API's module, and candidates are then enumerated from the parent subpackage of the deeper of the deprecated and replacement FQNs, keeping the search within a concrete subpackage.

For example, if the deeper FQN is:

```text
lib.pkg.module.dep_api
```

the candidate scope is the parent subpackage `lib.pkg`, and same-granularity candidate APIs are searched for in each release. The resulting candidate-mapping sizes used during scenario construction are:

| API Granularity | Candidate Mappings / Total Mappings |
|---|---:|
| class | 153 / 207 |
| function | 190 / 239 |
| method | 380 / 384 |
| **Total** | **723** |

To distinguish the effects of target-release evolution from those of initial-release variation, RQ2 constructs two migration scenarios.

### D-fixed (`fix_D`)

- Deprecated API fixed: use the deprecated API from the final pre-announcement release (or the release before removal if the definition was already removed);
- Candidate APIs evolve across releases: start from the announcement release and advance through the tenth post-removal release;
- If fewer than ten later releases are available, use the last available release as the cutoff.

This scenario fixes the initial API and observes how similarity and ranking change as the target release and its candidates evolve.

### R-fixed (`fix_R`)

- Candidate API fixed: use the candidate API from the removal release;
- Deprecated API evolves across releases: start from the tenth pre-announcement release, or the earliest available release, and continue through the final pre-removal release;
- This scenario fixes the target API and observes how similarity changes as the initial API evolves.

Release points without the definition required by the evolving API are excluded. To ensure sufficient data for trend analysis, a complete sequence must contain at least ten valid points across the two lifecycle periods.

The resulting experiment set is:

```text
D-fixed scenarios: 529
R-fixed scenarios: 443
Covered API mappings: 557
```

## 2. Input Files

The five Excel files in this directory belong to two groups.

### 2.1 Candidate-scope filtering results

```text
filter_cases_class.xlsx
filter_cases_function.xlsx
filter_cases_method.xlsx
```

These files correspond to the class, function, and method granularities. They record the API mappings and version information retained after the candidate scope was constrained, and serve as the data basis for candidate-scope construction and scenario filtering.

### 2.2 Final experimental-scenario data

```text
experimental_cases_fix_D.xlsx
experimental_cases_fix_R.xlsx
```

These files correspond to the `fix_D` and `fix_R` migration scenarios, respectively. They contain the API mappings, version boundaries, and candidate-version information used in the subsequent experiments.

## 3. Use in Subsequent Analyses

These Excel files are used by the later RQ2 modules:

- `lookup_source_def`: extracts deprecated-API and candidate-API source code from the API mappings and version information;
- `measure_similarity`: computes similarity and generates candidate rankings based on the candidate scope and migration scenarios;
- `RQ2.1`: organizes the similarity rankings and analyzes their trends across versions;
- `RQ2.2`: identifies key versions, attributes their causes, and analyzes candidate-API changes;
- `RQ2.3`: further identifies analysis change blocks and summarizes code change patterns from the key versions.
