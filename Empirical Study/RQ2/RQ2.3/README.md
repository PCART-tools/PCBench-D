RQ2.3 analyzes **code change patterns** in API migrations. The analysis uses key-version cases identified and classified in RQ2.2, focusing on:

1. Which code change blocks meet the analysis criteria for the observed ranking responses, including cases with no rank change;
2. The direction of influence that different analysis change blocks have under the `mapBased`, `tokenBased`, and `treeBased` algorithms;
3. Which concrete code change patterns can be summarized from these analysis change blocks;
4. How different change patterns are distributed across migration scenarios, dominant-cause categories, and API granularities.

This directory uses the implementation identifiers `mapBased`, `tokenBased`, and `treeBased` for the paper's **graph-based**, **token-based**, and **tree-based** algorithms, and the cause-directory names `dep_rep`, `common_cause`, and `candidates_cause` for the paper's **pair-dominant**, **mixed**, and **other-candidate-dominant** categories. The code and output field `core_blocks` refer to what the paper calls **analysis change blocks**; this label includes blocks selected when the original rank is unchanged.

---

## 1. Input Data

### 1.1 Case analysis results from RQ2.2

The upstream data for RQ2.3 comes from:

```text
Empirical Study/RQ2/RQ2.2/cases_split/
```

Cases under `cases_split` are organized by dominant cause, migration scenario, consistency category, and API granularity:

```text
cases_split/
├── candidates_cause/
│   ├── fix_D/
│   └── fix_R/
├── common_cause/
│   ├── fix_D/
│   └── fix_R/
└── dep_rep/
    ├── fix_D/
    └── fix_R/
```

Each case typically contains:

```text
<case>/
├── analysis.md
├── result/
│   ├── Vi-1_*/
│   └── Vi_*/
└── diff_analysis/
    ├── new.py
    ├── target.py
    └── block_*.patch
```

Here:

- `new.py`: the API source after the change;
- `target.py`: the target API source used for comparison;
- `block_*.patch`: individual blocks obtained by splitting the code changes;
- `analysis.md`: information such as version-rank changes, thresholds, and the replacement API;
- `result/`: similarity-ranking results for the `Vi-1` and `Vi` stages (the release before the key version and the key version itself).

### 1.2 Core change-block data

The four scripts in this directory analyze the cases under `cases_split` by:

- computing ranking changes after reversing each block;
- selecting blocks according to the restoration response, including blocks with no rank response;
- assigning labels to core blocks according to the influence direction under different algorithms.

The analysis results are written to the corresponding case file:

```text
<case>/diff_analysis/block_analysis.json
```

The file mainly contains:

- `blocks`: analysis results for all change blocks;
- `core_blocks`: core blocks selected for each algorithm;
- `block_sign_labels`: combined direction labels for core blocks.

### 1.3 Categorized change-pattern data

Core change blocks are organized by label under:

```text
Empirical Study/RQ2/RQ2.3/core_blocks/
```

A typical structure is:

```text
core_blocks/
├── fix_D/
│   └── dep_rep/
│       ├── class/
│       │   └── <block-label>/
│       ├── function/
│       └── method/
└── fix_R/
    ├── candidates_cause/
    ├── common_cause/
    └── dep_rep/
        ├── class/
        ├── function/
        └── method/
```

Each label directory contains:

- `.patch` files: the corresponding core code-change blocks;
- `.type` files: change-pattern labels assigned manually after analyzing each patch;
- `total.mode`: counts of the change patterns under the label directory.

---

## 2. Analysis Process

RQ2.3 consists of an automated analysis stage and a manual categorization stage.

### Automated analysis

1. `1. analyze_fix_D_blocks.py` analyzes each change block in the `fix_D` scenario;
2. `1. analyze_fix_R_blocks.py` analyzes each change block in the `fix_R` scenario;
3. `2. compute_core_blocks.py` selects analysis change blocks according to the original and restored ranking responses;
4. `3. label_block_signs.py` generates combined labels from the influence directions under different algorithms.

### Manual categorization

After the core blocks are organized by label under `core_blocks/`, the `.patch` files are inspected manually. The corresponding change patterns are then written to the `.type` files.

### Statistical analysis

The manually assigned patterns in the `.type` files are counted by migration scenario, dominant-cause category, API granularity, and change pattern. The final statistics are stored in the repository-provided file:

```text
mode_stats.xlsx
```

This generated result file is included in the repository.

---

## 3. Output Data Interpretation

### 3.1 `block_analysis.json`

This file records the influence analysis of each code-change block in a case.

Important fields include:

- `delta_vi1_to_vi`: the original ranking change from `Vi-1` to `Vi`;
- `baseline`: the baseline rank calculated from the `Vi-1` similarity score;
- `blocks`: the restoration results for each change block;
- `core_blocks`: core blocks selected for each algorithm;
- `block_sign_labels`: influence-direction labels for the core blocks.

A block entry typically looks like:

```json
{
  "block": "block_001",
  "patch_ok": true,
  "algorithms": {
    "mapBased": {
      "vi_rank": 10,
      "restored_score": 0.68,
      "restored_rank": 14,
      "delta_vi_to_restored": -4
    }
  }
}
```

### 3.2 `core_blocks`

`core_blocks` contains the core change blocks selected automatically:

```json
{
  "core_blocks": {
    "mapBased": ["block_001", "block_004"],
    "tokenBased": ["block_002"],
    "treeBased": ["block_005"]
  }
}
```

Core blocks are selected according to the relationship between `delta_vi_to_restored` and the direction of the original ranking change.

### 3.3 `block_sign_labels`

This field combines the influence directions of a block under different algorithms into one label. For example:

```text
map_up_token_down_tree_flat
```

The `up`, `down`, and `flat` labels describe the **effect of the change block itself on similarity ranking**, rather than the direct effect of reversing the change block. Since `delta_vi_to_restored` is obtained by comparing the current version with the version restored after removing the block, the block's influence direction is opposite to the effect of the restoration operation:

- `delta > 0`: removing the block lowers the numeric rank and improves the ranking, so the block itself worsens the ranking and is labeled `down`;
- `delta < 0`: removing the block raises the numeric rank and worsens the ranking, so the block itself improves the ranking and is labeled `up`;
- `delta = 0`: removing the block does not change the ranking, so the block is labeled `flat`.

### 3.4 `.patch` and `.type`

- `.patch`: the automatically extracted code change, used for manual analysis;
- `.type`: the change pattern manually assigned to the patch;
- `total.mode`: counts of the patterns under a label directory.

### 3.5 `mode_stats.xlsx`

`mode_stats.xlsx` contains the final statistics of the change patterns.

The current headers are:

```text
Scene | Root Cause | Granularity | Category | Change Mode | Count
```

| Field | Meaning |
|---|---|
| `Scene` | Migration scenario (`fix_D` / `fix_R`, the paper's D-fixed / R-fixed) |
| `Root Cause` | Dominant cause (the paper's pair-dominant / mixed / other-candidate-dominant), recorded as `dep_rep` / `common_cause` / `candidates_cause` |
| `Granularity` | API granularity: `class`, `function`, or `method` |
| `Category` | Category to which the change pattern belongs |
| `Change Mode` | Concrete code change pattern |
| `Count` | Number of occurrences of the change pattern |

---

# 1. analyze_fix_D_blocks.py

## 1. Overview

This script analyzes the influence of code-change blocks on replacement-API ranking in the `dep_rep/fix_D` scenario.

It:

1. Reads ranking results for `Vi-1` and `Vi`;
2. Reads `new.py`, `target.py`, and `block_*.patch`;
3. Applies each patch in reverse to restore the code with that change block removed;
4. Recomputes similarity with `mapBased`, `tokenBased`, and `treeBased`;
5. Recomputes the replacement API's rank;
6. Outputs the restored rank and influence of each block.

## 2. Usage

```bash
python "1. analyze_fix_D_blocks.py"
```

The script has no command-line arguments. Its input directory is determined by the `BASE` configuration in the code.

## 3. Input Parameters

Each case should contain:

```text
<case>/
├── analysis.md
├── result/Vi-1_*/
├── result/Vi_*/
└── diff_analysis/
    ├── new.py
    ├── target.py
    └── block_*.patch
```

`analysis.md` must provide algorithm ranking changes, thresholds, and the replacement API.

## 4. Output Structure

Results are written to:

```text
<case>/diff_analysis/block_analysis.json
```

The script also generates the runtime log:

```text
analyze_fix_D_blocks.log
```

---

# 1. analyze_fix_R_blocks.py

## 1. Overview

This script analyzes the influence of code-change blocks in `fix_R` cases under the `dep_rep`, `candidates_cause`, and `common_cause` categories.

Like `analyze_fix_D_blocks.py`, it:

- reverses each code-change block;
- recomputes similarity between the restored API and the candidates;
- recomputes the replacement API's rank;
- saves the ranking change for each block.

It pre-builds candidate representations and uses a process pool for parallel similarity computation.

## 2. Usage

```bash
python "1. analyze_fix_R_blocks.py"
```

## 3. Input Parameters

The script processes cases under:

```text
cases_split/dep_rep/fix_R/
cases_split/candidates_cause/fix_R/
cases_split/common_cause/fix_R/
```

Each case should contain `analysis.md`, `result/`, `R_candidates/`, and `diff_analysis/`.

## 4. Output Structure

Each case produces:

```text
<case>/diff_analysis/block_analysis.json
```

The result contains:

- replacement-API version ranks;
- algorithm baselines;
- restored similarity and restored rank for each block;
- influence metrics such as `delta_vi_to_restored`.

---

# 2. compute_core_blocks.py

## 1. Overview

This script selects core change blocks from all blocks in `block_analysis.json` and writes them to the `core_blocks` field.

The selection rules are:

- if the original ranking change is positive, select the blocks with the smallest `delta_vi_to_restored` only when that value is negative; otherwise, no core block is selected for that algorithm;
- if the original ranking change is negative, select the blocks with the largest `delta_vi_to_restored` only when that value is positive; otherwise, no core block is selected for that algorithm;
- if the original ranking change is zero, select only the blocks whose `delta_vi_to_restored` is zero;
- all blocks tied at the selected value are retained;
- blocks whose patches failed are excluded.

## 2. Usage

Preview mode:

```bash
python "2. compute_core_blocks.py"
```

Apply the changes:

```bash
python "2. compute_core_blocks.py" --apply
```

## 3. Input Parameters

The script recursively reads:

```text
<case>/diff_analysis/block_analysis.json
```

The JSON must contain:

- `algorithms`;
- `delta_vi1_to_vi`;
- `blocks`.

## 4. Output Structure

With `--apply`, the original `block_analysis.json` is extended with:

```json
{
  "core_blocks": {
    "mapBased": ["block_002", "block_005"],
    "tokenBased": ["block_001"],
    "treeBased": ["block_003"]
  }
}
```

Without `--apply`, the script runs in dry-run mode and only previews the changes.

---

# 3. label_block_signs.py

## 1. Overview

This script generates combined labels for core blocks according to their `delta_vi_to_restored` values under different algorithms.

The direction mapping is:

| Delta | Label |
|---:|---|
| Greater than 0 | `down` |
| Less than 0 | `up` |
| Equal to 0 | `flat` |

For example:

```text
mapBased = -3
tokenBased = 2
treeBased = 0
```

produces:

```text
map_up_token_down_tree_flat
```

## 2. Usage

```bash
python "3. label_block_signs.py"
```

## 3. Input Parameters

The script recursively reads `block_analysis.json` files that already contain `core_blocks`:

```text
<case>/diff_analysis/block_analysis.json
```

It is normally run after:

```bash
python "2. compute_core_blocks.py" --apply
```

## 4. Output Structure

The script adds the following field to the original `block_analysis.json`:

```json
{
  "block_sign_labels": {
    "map_up_token_down_tree_flat": [
      "block_001",
      "block_004"
    ]
  }
}
```

The labels can then be used to copy core patches into the corresponding label directories under `core_blocks/` for manual change-pattern categorization.
