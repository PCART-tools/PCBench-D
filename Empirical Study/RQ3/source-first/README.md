This directory contains API lifecycle cases classified as **source-first**. In these cases, the API's original source definition is removed while the original invocation remains executable, for example through aliases, re-exports, inheritance, or dynamic attribute resolution. If invocation failure is later observed, the source-definition removal version `Vd` is earlier than the original-invocation failure version `Vi`; otherwise, `Vi` remains unobserved at the lifecycle cutoff.

These cases are used to analyze why an API remains compatible or accessible after its source definition has been removed.

---

## 1. Data Structure

This directory contains three Excel files organized by API granularity:

```text
source-first/
├── class.xlsx
├── function.xlsx
└── method.xlsx
```

Each Excel file contains worksheets for individual libraries and a `summary` worksheet. The main columns in the data worksheets are:

```text
D_FQN | D_url | D_type | Va | Vd-1 | Vd | Vi | reason
```

The fields are:

- `D_FQN`: fully qualified name of the deprecated API;
- `D_url`: link to the API source definition;
- `D_type`: API granularity (`class`, `function`, or `method`);
- `Va`: deprecation-announcement version;
- `Vd-1`: version before source-definition removal;
- `Vd`: source-definition removal version;
- `Vi`: original-invocation failure version, produced in the data-collection stage;
- `reason`: manually verified compatibility mechanism or code evidence.

---

## 2. Statistics Overview

This directory currently contains **147 cases**.

### Distribution by API Granularity

| API Granularity | Cases | Percentage |
|---|---:|---:|
| class | 40 | 27.2% |
| function | 44 | 29.9% |
| method | 63 | 42.9% |
| **Total** | **147** | **100.0%** |

### Distribution by Granularity and Cause

| API Granularity | Compatibility through explicit aliases or re-exports | Method compatibility through inheritance | Dynamic attribute resolution | Same-named wrapper or namespace substitution | Total |
|---|---:|---:|---:|---:|---:|
| class | 34 | 0 | 1 | 5 | 40 |
| function | 39 | 0 | 3 | 2 | 44 |
| method | 11 | 52 | 0 | 0 | 63 |
| **Total** | **84** | **52** | **4** | **7** | **147** |

### Cause Descriptions

- **Compatibility through explicit aliases or re-exports** (84 cases, 57.1%): the original API continues to be exposed through explicit aliases, re-exports, or compatibility imports;
- **Method compatibility through inheritance** (52 cases, 35.4%): after the source definition is removed, the method remains available through a parent class or an inheritance relationship;
- **Dynamic attribute resolution** (4 cases, 2.7%): access continues to be provided through dynamic attribute-resolution mechanisms such as `__getattr__`;
- **Same-named wrapper or namespace substitution** (7 cases, 4.8%): the original access form is preserved through a same-named wrapper, namespace substitution, or API-type substitution.
