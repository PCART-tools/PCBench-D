RQ1.1 analyzes the source-definition location relationship between deprecated APIs and their maintainer-specified replacements. This informs the migration scope of replacements and provides a basis for the subsequent candidate-API search scope.

## 1. Overview

The script [fqn_classify.py](fqn_classify.py) classifies FQN mappings for class, function, and method granularities:

- class/function: compares module path and API name;
- method: compares module path, enclosing class, and method name;
- skips the `summary` worksheet;
- writes the classification result to the last column of each Excel worksheet.

## 2. Classification Rules

The categories below are the source-code location relationships reported in the paper's RQ1.1 (Table 4). They compare the two APIs' **source-definition-based FQNs**, i.e., FQNs built from each API's actual source definition rather than from changelog text. The `type` labels are numbered independently for the class/function group and the method group, so a label such as `type1` means different things in the two groups.

### Class and function

The FQN is split by `.`; the last segment is treated as the API name, and the remaining segments as the module path. The classification is:

| Type | Meaning |
|---|---|
| `type0` | identical: same name and same module path |
| `type1` | same name, different module: same name but different module |
| `type2` | different name, same module: same module but different name |
| `type3` | different name and module: different name and different module |

### Method

A method FQN has the form:

```text
module[.module...].ClassName.method_name
```

The classification is:

| Type | Meaning |
|---|---|
| `type1` | same module and class, different method name |
| `type2` | same module, different class, same method name |
| `type3` | same module, different class and method name |
| `type4` | different module, same method name |
| `type5` | different module and method name |

Two identical method FQNs are treated as an error case; the script writes an error message rather than a valid type.

## 3. Usage

The script requires the environment specified in `../environment.yml`. From this directory, create and activate it with:

```bash
conda env create -f ../environment.yml
conda activate pandas_tool
```

Using the default `input/` and `output/` directories:

```bash
python fqn_classify.py
```

Specifying input and output directories:

```bash
python fqn_classify.py \
    --input F:/path/to/input \
    --output F:/path/to/output
```

## 4. Input Parameters

### Command-line arguments

| Argument | Required | Description |
|---|---|---|
| `--input` | Optional | Input Excel directory, defaults to `input/` next to the script |
| `--output` | Optional | Output Excel directory, defaults to `output/` next to the script |

### Input files

The script identifies granularity by filename:

```text
input/class.xlsx
input/function.xlsx
input/method.xlsx
```

Columns 1 and 2 (`D_FQN` and `R_FQN`) of each workbook contain the deprecated-API FQN and replacement-API FQN to compare. The first row is treated as the header.

## 5. Output Structure

Output files keep their original names and are written to `output/`:

```text
output/
├── class.xlsx
├── function.xlsx
└── method.xlsx
```

The script writes `types` (or reuses an existing `result` / `types` column) into the last column of each data worksheet. Example cell values:

```text
type0
type1
type2
type3
type4
type5
```

Empty FQNs are not classified; identical method FQNs or other classification errors produce an error message beginning with `ERROR:`.
