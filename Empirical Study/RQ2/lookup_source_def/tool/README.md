This directory contains two modules used by the RQ2 source-extraction pipeline to **extract API source code**. Both primarily use Python's `ast` module, while `extract_dep.py` falls back to `parso` for Python 2 syntax.

---

## 1. extract_dep.py

### Purpose

This module **fetches and extracts the complete source code of a single specific API (function, class, or method) remotely via a GitHub URL**. Its main use case is: in a networked environment, given the GitHub link and fully qualified name of a deprecated API, precisely extract that API's code definition (preserving decorators, etc.) at the target version, returning a string for downstream use.

### Core API

`get_api_source_by_url_fqn_version_type(url, fqn, version, api_type, timeout=20)`

#### Inputs

- **`url`** (`str`): the original GitHub blob URL (e.g. `https://github.com/owner/repo/blob/master/path/file.py`); may carry a `#Lxx-Lyy` line suffix, which the module strips automatically.
- **`fqn`** (`str`): the API's fully qualified name.
  - Function or class: e.g. `jax.random.normal`.
  - Method: must include the class name, e.g. `ClassName.method_name`.
- **`version`** (`str`): the target version to extract (e.g. `v1.2.0`); the module substitutes it into the corresponding level of the original URL.
- **`api_type`** (`int`): the extraction granularity.
  - `1`: function
  - `2`: class
  - `3`: method
- **`timeout`** (`int`, optional): network request timeout, default 20 seconds.

#### Outputs

- **`str`**: the complete source code of the target API (plain text).
- **Exceptions**: `ValueError` is raised for an invalid URL format or when the requested API cannot be found. Network and HTTP failures are propagated as `requests` exceptions.

---

## 2. extract_and_save_rep.py

### Purpose

This module **bulk-scans a local Git repository and extracts all candidate API source code at a specified version, saving them as local files**. Its main use case is: on a local machine, automatically switch the whole codebase to a given tag version, walk all Python files, extract all functions/classes/methods, and save each as a standalone `.py` file named by its fully qualified name — to build the candidate API pool for a new version.

### Core API

`extract_candidates(root, libname, version, path, type, outputRoot)`

#### Inputs

- **`root`** (`str | Path`): the root directory holding the codebase (e.g. `/root/repos`).
- **`libname`** (`str`): the repository directory name (e.g. `jax`). The actual full repository path is `root/libname`.
- **`version`** (`str`): the target version (e.g. `v1.2.0`); the script runs `git checkout tags/<version>` locally.
- **`path`** (`str`): the relative subpath inside the repository to scan (e.g. `jax/_src`). Passing `""` or `.` scans the whole repository.
- **`type`** (`int`): the extraction granularity.
  - `1`: function
  - `2`: class
  - `3`: method
- **`outputRoot`** (`str | Path`): the output directory for the extracted results.

#### Outputs

- **`List[Path]`**: paths of all API source files successfully extracted and written to disk (e.g. `[Path('/output/jax._src.random.normal.py'), ...]`).
- **File artifacts**: under `outputRoot`, a series of files named `fully.qualified.name.py`, each containing the complete source of that API.
