RQ1.2 analyzes the parameter-interface differences between deprecated APIs and their maintainer-specified replacements, to understand which parameter changes need to be handled during invocation adaptation.

## 1. Overview

The script [do_analyze.py](do_analyze.py) uses PCART (a Python API parameter-change analysis tool) to compare the parameter signatures of deprecated and replacement APIs, identifying additions, removals, renamings, type changes, position changes, and conversions between positional and keyword arguments.

For each worksheet row, the script:

1. Reads the deprecated-API and replacement-API signature text from columns 6 and 7;
2. Extracts the outermost parenthesized content of each signature;
3. Calls PCART's `findDiffer` to compare the two parameter signatures;
4. Writes the analysis result into column 9.

## 2. Parameter Sources

- Functions and methods: parameter lists come from their definitions;
- Classes: parameter lists come from a custom metaclass's `__call__`; if absent, the first available `__new__` or `__init__` is used; a class's own `__call__` describes instance invocation and is excluded.

## 3. Excluded Mappings

99 mappings with ambiguous parameter correspondence are excluded from the parameter-difference summary statistics.

For example, a change from `glm(data, para)` to `ttest_ind(a, b, axis=0, equal_var=True)` may simultaneously involve parameter renaming, addition, and removal, which parameter-level evidence alone cannot distinguish reliably. Such mappings are therefore excluded from the parameter-difference statistics.

## 4. Result Classification

The remaining mappings are reported by granularity as:

- identical parameter lists;
- exactly one change type;
- two change types;
- three change types;
- at least four change types.

For mappings with exactly one change type, the specific change type is further reported.

## 5. Usage

The script requires the environment specified in `../environment.yml`. From this directory, create and activate it with:

```bash
conda env create -f ../environment.yml
conda activate pandas_tool
```

```bash
python do_analyze.py \
    --input F:/path/to/class.xlsx \
    --out_dir F:/path/to/output
```

## 6. Input Parameters

### Command-line arguments

| Argument | Required | Description |
|---|---|---|
| `--input` | **Required** | Input Excel file path |
| `--out_dir` | **Required** | Output directory path |

### Input files

Columns 6 and 7 of the input Excel should contain the deprecated-API and replacement-API signature text, for example:

```text
(a: int, b=1) -> bool
```

The script extracts the outermost parenthesized content of these texts as the signatures to compare.

### PCART dependency

The script uses **PCART v1.3**. It loads PCART from a hard-coded path:

```text
/dataset/he/Rbench/R1/PCART/Change/changeAnalyze.py
```

When running in another environment, replace this path with the actual location of PCART's `changeAnalyze.py`.

## 7. Output Structure

For each input workbook, the script writes an analyzed workbook to the output directory:

```text
<stem>_analyzed.xlsx
```

For example, input `class.xlsx` produces `class_analyzed.xlsx`. In these analyzed workbooks, the script writes the PCART result to column 9. Cells that cannot be processed contain an error message, for example:

```text
{"error": "signature_not_found"}
{"error": "analyze_failed", "message": "..."}
```

The repository also contains aggregated summary tables under `output/`:

```text
output/
├── class.xlsx
├── function.xlsx
└── method.xlsx
```

These files summarize the analyzed results by API granularity. They are distinct from the per-input `_analyzed.xlsx` files produced directly by `do_analyze.py`.
