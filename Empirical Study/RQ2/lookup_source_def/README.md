This directory prepares the source-code data used by the RQ2 similarity study. It takes API-pair information from Excel, retrieves the deprecated API source from GitHub, extracts replacement-candidate APIs from local Git repositories, and optionally removes oversized candidate files.

## 1. Input Data Format

### Excel input

The input Excel workbook is stored under `input/`. Each worksheet represents one library, and the worksheet name is used as `libname`. The first row is the header. The workbook uses the following 11-column layout:

```text
A=D_FQN  B=R_FQN  C=D_type  D=Va-1  E=Vd  F=Vr  G=D_url  H=R_url
I=bef_n_versions  J=transition_versions  K=aft_n_versions
```

Here `Va-1` is the final pre-announcement release, `Vd` the source-definition removal version, and `Vr` the original-invocation failure version (the paper's D-1, S, and F); `bef_n_versions`, `transition_versions`, and `aft_n_versions` list the releases of the pre-deprecation, source-definition transition, and post-removal periods.

The extraction scripts use the following fields:

- `D_FQN`: fully qualified name of the deprecated API;
- `R_FQN`: fully qualified name of the replacement API;
- `D_url`: GitHub blob URL for the deprecated API source;
- `bef_n_versions`: comma-separated versions before the transition;
- `transition_versions`: comma-separated transition versions;
- `aft_n_versions`: comma-separated versions after the transition.

### Local Git repositories

A local Git repository is required for each worksheet/library. The repository must be located at:

```text
<repo_root>/<libname>/
```

It must contain Git tags corresponding to the versions listed in the Excel file, because candidate extraction checks out `tags/<version>` for each requested version.

The deprecated-API extraction also requires network access to the corresponding GitHub raw-content URLs.

## 2. Execution Workflow

Run the scripts in the following order:

1. **Extract source code** with `extract_and_save.py`:
   - read the Excel cases;
   - fetch the deprecated API definitions from GitHub for the requested versions;
   - check out the corresponding tags in the local repositories;
   - extract replacement candidates from the local repositories;
   - optionally run `trim_large_candidates.py` when prompted.
2. **Optional cleanup** with `trim_large_candidates.py` if large-candidate cleanup was not performed during extraction. Oversized files are moved, not deleted.
3. **Optional rollback** with `restore_del_candidates.py` when the moved candidate files need to be restored to `R_candidates`.
4. **Use the generated source-code directory** as the input for the downstream similarity-measurement pipeline.

The `api_type` argument used by `extract_and_save.py` determines the extraction granularity:

- `1`: function;
- `2`: class;
- `3`: method.

## 3. Final Output Structure

After source extraction, the main output has the following structure:

```text
<output_dir>/<function|class|method>/<subpath or auto-number>/
├── <libname>/
│   ├── <fqn_D>-<fqn_R>/
│   │   ├── <fqn_D>/
│   │   │   ├── <version1>.py       # deprecated API source from GitHub
│   │   │   └── <version2>.py
│   │   └── R_candidates/
│   │       ├── <version1>/
│   │       │   ├── <fully.qualified.name>.py
│   │       │   └── ...             # replacement candidates from local Git
│   │       └── <version2>/
│   └── ...
└── <libname2>/...
```

If large-candidate cleanup is run, the following additional artifacts may appear:

```text
<case>/
├── del_candidates/<version>/       # oversized candidate files moved here
├── del_candidates/del.log          # per-version cleanup statistics
└── ...
<output_dir>/del_candidates_summary.log
```

The detailed descriptions of the individual scripts follow.

---

# extract_and_save.py

This script is the **main orchestration script** in the `lookup_source_def` directory. It reads "deprecated API → replacement API" pair cases in bulk from an Excel file and extracts the source code for both sides to disk, preparing the source-code dataset for RQ2 (the study of similarity between deprecated and replacement APIs).

---

## 1. Overview

The script reads an Excel workbook (each sheet corresponds to one library) and, for each row (one case):

- **Deprecated API**: fetches the source definition of the API at the specified version **remotely from GitHub**, using the GitHub link + fully qualified name + version number from the Excel file;
- **Replacement candidates**: extracts, in bulk, all same-granularity APIs at the specified version **from a locally cloned Git repository**, using the inferred repository subpath + version number, forming a candidate pool.

The extraction granularity is controlled by `--api_type` (function / class / method). The whole process supports resumability (completed files/directories are automatically skipped).

---

## 2. Usage

```bash
# Extract source at the class granularity
python extract_and_save.py \
    --excel input/class_no_transition.xlsx \
    --api_type 2 \
    --output_dir /path/to/output \
    --repo_root /path/to/repos
```

```bash
# Extract at the method granularity, using default output/repo directories
python extract_and_save.py --excel input/method_transition.xlsx --api_type 3
```

There are two interactive prompts during the run:

1. **Output subpath**: press Enter directly → auto-numbered by the existing directory count (0, 1, 2…); type a custom string → used as the subdirectory name;
2. **Whether to run large-file cleanup**: type `y`/`yes` → run `trim_large_candidates`; anything else → skip.

> Note: the defaults for `--output_dir` and `--repo_root` (`/media/he/Rbench/similarity/output`, `/dataset/he`) are paths from the original Linux development environment. On a supported Linux filesystem, pass paths for your own output and local repository directories explicitly.

---

## 3. Input Parameters

### Command-line arguments

| Argument | Required | Description |
|---|---|---|
| `--excel` | **Required** | Path to the input Excel file. Each sheet name = library name (libname); see the column layout below |
| `--api_type` | **Required** | Extraction granularity: `1` = function, `2` = class, `3` = method |
| `--output_dir` | Optional | Root directory for extracted source (default `/media/he/Rbench/similarity/output`) |
| `--repo_root` | Optional | Root directory of local Git repositories (default `/dataset/he`) |

### Required external resources

- **Excel file** (required): the header must be the following 11 columns (i.e., the unified structure under `input/`):

  ```
  A=D_FQN  B=R_FQN  C=D_type  D=Va-1  E=Vd  F=Vr  G=D_url  H=R_url
  I=bef_n_versions  J=transition_versions  K=aft_n_versions
  ```

  The script actually uses 6 columns: `A` (deprecated API's fully qualified name), `B` (replacement API's fully qualified name), `G` (deprecated API's GitHub blob URL), `I` (before versions), `J` (transition versions), `K` (after versions).

- **Local Git repository** (required): the repository is located at `repo_root/<libname>` (where `libname` is the Excel sheet name), and **must have tags matching the version numbers** (the script runs `git checkout tags/<version>`). For example, to extract version `v2.0.0` of `jax`, `repo_root/jax` must have the `v2.0.0` tag.

### Other dependencies

- Network access to `raw.githubusercontent.com` (remote fetching of deprecated APIs, with retries);
- Python packages: `openpyxl`, `requests`, `urllib3` (`parso` optional, for Python 2 syntax fallback);
- Local modules: `tool/extract_dep.py`, `tool/extract_and_save_rep.py`, `trim_large_candidates.py`.

### Meaning of `api_type`

- `1` (function): extract top-level functions (including `async def`);
- `2` (class): extract class definitions;
- `3` (method): extract methods defined directly inside a class, located by "ClassName.method_name" (two segments).

`api_type` affects: ① how the FQN is parsed into a function/class/method name during remote extraction; ② the granularity of local candidate extraction; ③ the repository subpath derived by `compute_prefix` from the deeper of the deprecated and replacement FQNs (dropping 3 trailing segments for methods, 2 for functions/classes); ④ the output subdirectory name (`function` / `class` / `method`).

---

## 4. Output Structure

```
<output_dir>/<function|class|method>/<subpath or auto-number>/
├── <libname>/                          # one directory per library (= Excel sheet name)
│   ├── <fqn_d>-<fqn_r>/                # one directory per case
│   │   ├── <fqn_d>/                    # deprecated API source (remote)
│   │   │   ├── <version1>.py
│   │   │   └── <version2>.py           # one file per deprecated version (filename = version)
│   │   └── R_candidates/               # replacement candidate source (local)
│   │       ├── <version1>/             # one directory per candidate version
│   │       │   ├── <fully.qualified.name>.py   # e.g. jax._src.random.normal.py
│   │       │   └── ...
│   │       └── <version2>/...
│   └── ...
├── <libname2>/...
└── (if trim cleanup is run)
    ├── del_candidates/<version>/ under each case   # oversized files moved here
    ├── del_candidates/del.log under each case      # per-version threshold & move stats
    └── del_candidates_summary.log                  # root-level summary (rows with moved>0)
```

**Notes**:

- Deprecated API: **one `.py` file per version** (filename = version number);
- Replacement candidates: **one subdirectory per version**, each containing files named `fully.qualified.name.py`;
- The log file `<Excel-name>.log` is written to the **script's own directory** (not inside `output_dir`);
- Trim cleanup *moves* files rather than deletes them; it can be rolled back with `restore_del_candidates.py`.

---

# trim_large_candidates.py

This script **cleans up oversized files in the candidate pool**: it walks `root/libname/case/R_candidates/<version>`, counts the effective code lines of each `.py` file per version directory, moves candidates exceeding the threshold into `del_candidates`, and records statistics. It is usually offered at the end of `extract_and_save.py`, but can also be run standalone.

## 1. Overview

For the `root/libname/case/R_candidates/<version>` structure:

1. Uses `py_line_stats` to count effective code lines of all `.py` files in that version directory, obtaining p60/p80/p90 percentile thresholds;
2. Computes the move threshold `thr = max(p90×5, p60×10, 1000)`;
3. Moves files whose line count exceeds `thr` to `case/del_candidates/<version>/` (name collisions get a `__dupN` suffix);
4. Records per-version thresholds and move statistics in `del_candidates/del.log`;
5. Aggregates rows with `moved>0` from all cases' `del.log` files into the root-level `del_candidates_summary.log`.

## 2. Usage

```bash
# Clean all oversized candidates under an output root directory
python trim_large_candidates.py /path/to/output
```

## 3. Input Parameters

| Argument | Required | Description |
|---|---|---|
| `root_dir` (positional) | **Required** | Root directory; the next level is libnames, with the structure `root/libname/case/R_candidates/<version>/` |

- Depends on the sibling `py_line_stats.py` (`analyze_py_line_counts`, `count_effective_code_lines`, `read_text_best_effort`).
- Threshold rule: `thr = max(p90×5, p60×10, 1000)`.
- Files are *moved*, not deleted; roll back with `restore_del_candidates.py`.

## 4. Output Structure

```
root/
├── <libname>/<case>/
│   ├── R_candidates/<version>/        # after cleanup keeps only files with lines <= thr
│   └── del_candidates/
│       ├── <version>/                  # oversized files moved here
│       └── del.log                     # one stats line per version
│           # format: version | p60=... | p80=... | p90=... | thr=... | moved=... | min=... | avg=...
└── del_candidates_summary.log          # root-level summary (rows with moved>0, prefixed with libname | case)
```

---

# restore_del_candidates.py

This script is the **reverse / rollback tool for `trim_large_candidates.py`**: it moves candidate files back from `del_candidates` to `R_candidates` and removes the `del_candidates` directory.

## 1. Overview

Walks `root/libname/case/del_candidates/<version>`:

1. Moves each `.py` file back to `case/R_candidates/<version>/`;
2. On name collision, appends a `__restoredupN` suffix;
3. After all files are moved, deletes the whole `del_candidates` directory.

## 2. Usage

```bash
# Undo a trim cleanup
python restore_del_candidates.py /path/to/output
```

## 3. Input Parameters

| Argument | Required | Description |
|---|---|---|
| `root_dir` (positional) | **Required** | Root directory; the next level is libnames, with the structure `root/libname/case/del_candidates/<version>/` |

- No third-party dependencies (stdlib only: `argparse`, `shutil`, `pathlib`).

## 4. Output Structure

- Moved `.py` files return to `case/R_candidates/<version>/`;
- The `case/del_candidates/` directory is deleted;
- The console prints each `libname/case` being processed.

---

# py_line_stats.py

This script is a **line-counting utility**: it counts the "effective code lines" (excluding blank lines and comments) of all `.py` files in a directory and computes percentile and rank thresholds. It is also reused by `trim_large_candidates.py` as the threshold-computing dependency.

## 1. Overview

1. Reads all `.py` files in the target directory (multi-encoding fallback: utf-8 / utf-8-sig / latin-1);
2. Counts effective code lines of each file with `tokenize` (ignoring comments, blank lines, indentation, etc.);
3. Computes 60%/70%/80%/90% percentile thresholds;
4. Computes rank thresholds: `max`, `top_10` … `top_100`.

## 2. Usage

```bash
# Count the line distribution of .py files in a directory
python py_line_stats.py /path/to/dir
```

## 3. Input Parameters

| Argument | Required | Description |
|---|---|---|
| `directory` (positional) | **Required** | Directory to analyze (**only the current level, non-recursive**) |

- No third-party dependencies (stdlib: `argparse`, `io`, `math`, `tokenize`, `pathlib`).

## 4. Output Structure

Prints to console (nothing written to disk):

```
Percentile thresholds (the proportion of files with line count <= the value):
  60%: N lines
  70%: N lines
  80%: N lines
  90%: N lines
Rank thresholds:
  max: N lines
  top_10: N lines
  ...
  top_100: N lines
```
