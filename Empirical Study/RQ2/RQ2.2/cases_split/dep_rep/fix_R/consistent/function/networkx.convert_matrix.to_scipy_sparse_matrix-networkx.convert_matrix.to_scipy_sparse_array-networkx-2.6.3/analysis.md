# 一、突变情况分析

- **Total**: 2299
- **替代API**: `networkx.convert_matrix.to_scipy_sparse_array`
- **10% 阈值**: 229.9

## Vi-1 (networkx-2.6.3-networkx-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9983 |
| tokenBased | 1 | 0.9784 |
| treeBased | 1 | 0.9916 |

## Vi (networkx-2.7-networkx-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1716 | 0.2381 |
| tokenBased | 1870 | 0.1619 |
| treeBased | 2025 | 0.2321 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 1716 | -1715 | true |
| tokenBased | 1 | 1870 | -1869 | true |
| treeBased | 1 | 2025 | -2024 | true |

```json
{
  "total": 2299,
  "replacement_api": "networkx.convert_matrix.to_scipy_sparse_array",
  "threshold_10pct": 229.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.998344
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.978417
    },
    "treeBased": {
      "rank": 1,
      "score": 0.991611
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1716,
      "score": 0.238108
    },
    "tokenBased": {
      "rank": 1870,
      "score": 0.161871
    },
    "treeBased": {
      "rank": 2025,
      "score": 0.232092
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 1716,
      "delta": -1715,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 1870,
      "delta": -1869,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 2025,
      "delta": -2024,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `networkx.convert_matrix.to_scipy_sparse_matrix/Vi-1_networkx-2.6.3.py`
- **new**: `networkx.convert_matrix.to_scipy_sparse_matrix/Vi_networkx-2.7.py`
- **+11 / -50**

```diff
--- networkx.convert_matrix.to_scipy_sparse_matrix/Vi-1_networkx-2.6.3.py
+++ networkx.convert_matrix.to_scipy_sparse_matrix/Vi_networkx-2.7.py
@@ -3,54 +3,15 @@
     import scipy as sp
     import scipy.sparse
 
-    if len(G) == 0:
-        raise nx.NetworkXError("Graph has no nodes or edges")
-
-    if nodelist is None:
-        nodelist = list(G)
-        nlen = len(G)
-    else:
-        nlen = len(nodelist)
-        if nlen == 0:
-            raise nx.NetworkXError("nodelist has no nodes")
-        nodeset = set(G.nbunch_iter(nodelist))
-        if nlen != len(nodeset):
-            for n in nodelist:
-                if n not in G:
-                    raise nx.NetworkXError(f"Node {n} in nodelist is not in G")
-            raise nx.NetworkXError("nodelist contains duplicates.")
-        if nlen < len(G):
-            G = G.subgraph(nodelist)
-
-    index = dict(zip(nodelist, range(nlen)))
-    coefficients = zip(
-        *((index[u], index[v], wt) for u, v, wt in G.edges(data=weight, default=1))
+    warnings.warn(
+        (
+            "\n\nThe scipy.sparse array containers will be used instead of matrices\n"
+            "in Networkx 3.0. Use `to_scipy_sparse_array` instead."
+        ),
+        DeprecationWarning,
+        stacklevel=2,
     )
-    try:
-        row, col, data = coefficients
-    except ValueError:
-
-        row, col, data = [], [], []
-
-    if G.is_directed():
-        M = sp.sparse.coo_matrix((data, (row, col)), shape=(nlen, nlen), dtype=dtype)
-    else:
-
-        d = data + data
-        r = row + col
-        c = col + row
-
-
-        selfloops = list(nx.selfloop_edges(G, data=weight, default=1))
-        if selfloops:
-            diag_index, diag_data = zip(*((index[u], -wt) for u, v, wt in selfloops))
-            d += diag_data
-            r += diag_index
-            c += diag_index
-        M = sp.sparse.coo_matrix((d, (r, c)), shape=(nlen, nlen), dtype=dtype)
-    try:
-        return M.asformat(format)
-
-
-    except (AttributeError, ValueError) as e:
-        raise nx.NetworkXError(f"Unknown sparse matrix format: {format}") from e
+    A = to_scipy_sparse_array(
+        G, nodelist=nodelist, dtype=dtype, weight=weight, format=format
+    )
+    return sp.sparse.csr_matrix(A).asformat(format)
```

```json
{
  "old_file": "networkx.convert_matrix.to_scipy_sparse_matrix/Vi-1_networkx-2.6.3.py",
  "new_file": "networkx.convert_matrix.to_scipy_sparse_matrix/Vi_networkx-2.7.py",
  "lines_added": 11,
  "lines_removed": 50
}
```
