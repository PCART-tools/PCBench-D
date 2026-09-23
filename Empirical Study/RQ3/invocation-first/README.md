This directory contains API lifecycle cases classified as **invocation-first**. In these cases, the original invocation fails while the API's source definition still exists. If removal is later observed, the original-invocation failure version `Vi` is earlier than the source-definition removal version `Vd`; otherwise, `Vd` remains unobserved at the lifecycle cutoff.

These cases are used to analyze why an API can no longer be invoked in its original manner even though its definition is still present in the source code.

---

## 1. Data Structure

This directory contains three Excel files organized by API granularity:

```text
invocation-first/
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
- `reason`: manually verified original-invocation failure cause or code evidence.

---

## 2. Statistics Overview

This directory contains **43 cases**, distributed by granularity as follows:

| API Granularity | Cases | Percentage |
|---|---:|---:|
| class | 17 | 39.5% |
| function | 19 | 44.2% |
| method | 7 | 16.3% |
| **Total** | **43** | **100.0%** |

### Distribution by Granularity and Cause

| API Granularity | Deprecated access path or public alias unavailable | Definition retained with explicit failure logic | Incompatible invocation contract | Repository definition inconsistent with runtime or package exposure | Total |
|---|---:|---:|---:|---:|---:|
| class | 3 | 7 | 4 | 3 | 17 |
| function | 17 | 0 | 0 | 2 | 19 |
| method | 0 | 2 | 2 | 3 | 7 |
| **Total** | **20** | **9** | **6** | **8** | **43** |

### Cause Descriptions

- **Deprecated access path or public alias unavailable** (20 cases, 46.5%): the source definition may still exist, but the original public access path, short alias, or exposure mechanism is no longer available;
- **Definition retained with explicit failure logic** (9 cases, 20.9%): the source definition remains, but explicit failure logic has been added to the function body or implementation, causing invocation to fail actively;
- **Incompatible invocation contract** (6 cases, 14.0%): the invocation method, parameter form, or interface contract has changed, so the previous invocation form is no longer compatible;
- **Repository definition inconsistent with runtime or package exposure** (8 cases, 18.6%): the definition remains in the repository, but the installed package, runtime namespace, or externally exposed content is no longer synchronized with it.
