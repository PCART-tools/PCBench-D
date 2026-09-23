A similarity algorithm based on **weighted token Jaccard**: it encodes API source code into a token sequence and then computes the similarity between two code snippets with weighted Jaccard. It is one of the three algorithms used by `compute_similarity.py`.

The three similarity algorithms are named **graph-based**, **token-based**, and **tree-based** in the paper; the repository implements them as the modules `mapBased`, `tokenBased`, and `treeBased`. This spelling is retained because the same identifiers appear in code, JSON output, and filenames.

---

## 1. Overview

1. Uses `APITokenizer` (an `ast.NodeVisitor`) to encode API source code into a **token sequence**, explicitly extracting structural information: definition kind, function/class name (word-split), parameter structure, parameter/return type annotations, decorators, and body structure such as control flow / calls / literals / containers — down-weighting the influence of local variable names and literal details;
2. Counts the token sequence into a multiset (`Counter`) and assigns different weights by token category;
3. Computes the similarity between two snippets with **weighted Jaccard** (`weighted_jaccard_similarity_from_counter`), returning a score in `[0, 1]`.

---

## 2. Usage

```python
from similarity.tokenBased import build_representation, similarity_from_representation

rep_a = build_representation(src_a)          # compile the query
rep_b = build_representation(src_b)          # compile the candidate
score = similarity_from_representation(rep_a, rep_b)   # -> float, [0, 1]
```

Compute directly from two source strings:

```python
from similarity.tokenBased import similarity
score = similarity(src_a, src_b)
```

---

## 3. Input Parameters

### `build_representation(source, name_weight=3.0, param_type_weight=4.0, return_type_weight=2.0, default_weight=1.0)`

| Parameter | Description |
|---|---|
| `source` (`str`) | The input Python source string |
| `name_weight` | Weight of function/class name signature tokens, default `3.0` |
| `param_type_weight` | Weight of parameter-type tokens, default `4.0` |
| `return_type_weight` | Weight of return-type tokens, default `2.0` |
| `default_weight` | Default weight of ordinary tokens, default `1.0` |

### `similarity_from_representation(repr_a, repr_b)`

| Parameter | Description |
|---|---|
| `repr_a` / `repr_b` | Two representation dicts produced by `build_representation` |

---

## 4. Output Structure

`build_representation` returns:

```python
{
    "algorithm": "tokenBased",
    "normalized_source": "...",      # normalized source
    "tokens": [...],                 # token list
    "counter": Counter(...),         # token multiset counts
    "weights": {...},                # per-category token weights
    "meta": {"token_count": ..., "unique_token_count": ...}
}
```

`similarity_from_representation` returns a `float` (the weighted Jaccard similarity in `[0, 1]`).

---

# treeBased.py

A similarity algorithm based on **AST tree edit distance (TED)**: it builds a lightweight AST tree from API source code, measures the difference via tree edit distance, and normalizes it into a similarity score. It is one of the three algorithms used by `compute_similarity.py`.

---

## 1. Overview

1. Builds a lightweight AST tree from API source code and computes the **tree edit distance (TED)** with `zss.simple_distance`;
2. Normalizes it into a `[0, 1]` similarity via `1 - ted/denom`;
3. **The module also implements hierarchical comparison for class APIs** (to avoid feeding a whole class into TED directly): a weighted combination of class-header TED (0.15) + class-attribute Jaccard (0.10) + method-set Jaccard (0.15) + matched-method TED coverage weighting (0.60). The paper's class-level experiments do not use tree-based similarity because tree-edit computation was infeasible for several large class definitions; they use token- and graph-based similarity only.

---

## 2. Usage

```python
from similarity.treeBased import build_representation, similarity_from_representation

rep_a = build_representation(src_a)
rep_b = build_representation(src_b)
score = similarity_from_representation(rep_a, rep_b)   # -> float, [0, 1]
```

Compute directly from two source strings:

```python
from similarity.treeBased import similarity
score = similarity(src_a, src_b)
```

---

## 3. Input Parameters

### `build_representation(src, keep_api_tree=False)`

| Parameter | Description |
|---|---|
| `src` (`str`) | A single API source string |
| `keep_api_tree` (`bool`) | Whether to also retain the `APITree` large object; unnecessary for most comparison scenarios |

### `similarity_from_representation(repr_a, repr_b)`

| Parameter | Description |
|---|---|
| `repr_a` / `repr_b` | Two representation dicts produced by `build_representation` |

### `detail_from_representation(repr_a, repr_b)`

Returns more detailed comparison info (including intermediate quantities such as `tree_edit_distance`).

---

## 4. Output Structure

`build_representation` returns a reusable representation (`BuiltTree`, containing `zss_node` / `size`, etc.; for class APIs it is a `BuiltClassRepresentation`, containing `header_tree` / `class_attributes` / `methods` / `size`).

`similarity_from_representation` returns a `float` (the TED-normalized similarity in `[0, 1]`).

---

# mapBased.py

A similarity algorithm based on a **simplified PDG (program dependency graph) structure**: it builds a simplified dependency graph from API source code and compares the structural similarity of two graphs. It is one of the three algorithms used by `compute_similarity.py`.

---

## 1. Overview

1. Builds a **simplified PDG** from API source code: node kinds such as `ENTRY` / `CALL` / `RETURN` / `NESTED_DEF`, and edge kinds `control` (control flow) / `data` (data flow);
2. **Functions/methods**: builds a function PDG `Graph` and compares two graphs with `_graph_similarity`;
3. **Classes**: builds a `ClassSummary` (class name, field set, and a PDG graph per method) and compares with `_class_similarity_from_summary`;
4. Representations are reusable: query / candidate are each compiled once, and subsequent comparisons don't re-parse or re-build the graph.

---

## 2. Usage

```python
from similarity.mapBased import build_representation, similarity_from_representation

rep_a = build_representation(src_a)
rep_b = build_representation(src_b)
score = similarity_from_representation(rep_a, rep_b)   # -> float, [0, 1]
```

Compute directly from two source strings:

```python
from similarity.mapBased import similarity
score = similarity(src_a, src_b)
```

---

## 3. Input Parameters

### `build_representation(api_src)`

| Parameter | Description |
|---|---|
| `api_src` (`str`) | The API source string (function/method/class) |

### `similarity_from_representation(repr_a, repr_b)`

| Parameter | Description |
|---|---|
| `repr_a` / `repr_b` | Two representation dicts produced by `build_representation` (must be both functions or both classes) |

---

## 4. Output Structure

`build_representation` returns:

```python
{
    "algorithm": "mapBased",
    "api_kind": "class" or "function",
    "normalized_source": "...",
    "representation": <Graph or ClassSummary>,
    "meta": {...}   # functions: node_count/edge_count/is_async; classes: class_name/field_count/method_count
}
```

`similarity_from_representation` returns a `float` (the graph similarity score in `[0, 1]`).

---

# py2_to_py3_converter.py

A **compatibility utility**: converts Python 2 source code to Python 3 in memory, used as a fallback when `ast.parse` cannot parse historical-version code.

---

## 1. Overview

`convert_py2_to_py3(source_code)` uses `lib2to3` (Python ≤ 3.12) or `fissix` (Python ≥ 3.13, where the stdlib has removed `lib2to3`) to convert Python 2 → 3 syntax, returning a valid Python 3 source string.

---

## 2. Usage

```python
from similarity.py2_to_py3_converter import convert_py2_to_py3

try:
    tree = ast.parse(src)
except SyntaxError:
    src = convert_py2_to_py3(src)   # fallback conversion, then re-parse
    tree = ast.parse(src)
```

---

## 3. Input Parameters

### `convert_py2_to_py3(source_code)`

| Parameter | Description |
|---|---|
| `source_code` (`str`) | The original source string that may contain Python 2 syntax |

---

## 4. Output Structure

Returns a `str`: the converted, valid Python 3 source string.

> Dependencies: Python ≤ 3.12 uses the stdlib `lib2to3`; Python ≥ 3.13 requires the third-party `fissix` (`pip install fissix`).
