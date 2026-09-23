# 一、突变情况分析

- **Total**: 2299
- **替代API**: `networkx.convert_matrix.from_scipy_sparse_array`
- **10% 阈值**: 229.9

## Vi-1 (networkx-2.6.3-networkx-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 1.0000 |
| treeBased | 1 | 0.9962 |

## Vi (networkx-2.7-networkx-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 624 | 0.3907 |
| tokenBased | 474 | 0.2500 |
| treeBased | 1393 | 0.2970 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 624 | -623 | true |
| tokenBased | 1 | 474 | -473 | true |
| treeBased | 1 | 1393 | -1392 | true |

```json
{
  "total": 2299,
  "replacement_api": "networkx.convert_matrix.from_scipy_sparse_array",
  "threshold_10pct": 229.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 1.0
    },
    "treeBased": {
      "rank": 1,
      "score": 0.996212
    }
  },
  "vi": {
    "mapBased": {
      "rank": 624,
      "score": 0.390705
    },
    "tokenBased": {
      "rank": 474,
      "score": 0.25
    },
    "treeBased": {
      "rank": 1393,
      "score": 0.29697
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 624,
      "delta": -623,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 474,
      "delta": -473,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 1393,
      "delta": -1392,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `networkx.convert_matrix.from_scipy_sparse_matrix/Vi-1_networkx-2.6.3.py`
- **new**: `networkx.convert_matrix.from_scipy_sparse_matrix/Vi_networkx-2.7.py`
- **+14 / -35**

```diff
--- networkx.convert_matrix.from_scipy_sparse_matrix/Vi-1_networkx-2.6.3.py
+++ networkx.convert_matrix.from_scipy_sparse_matrix/Vi_networkx-2.7.py
@@ -2,38 +2,17 @@
     A, parallel_edges=False, create_using=None, edge_attribute="weight"
 ):
     
-    G = nx.empty_graph(0, create_using)
-    n, m = A.shape
-    if n != m:
-        raise nx.NetworkXError(f"Adjacency matrix not square: nx,ny={A.shape}")
-
-    G.add_nodes_from(range(n))
-
-
-    triples = _generate_weighted_edges(A)
-
-
-
-
-
-    if A.dtype.kind in ("i", "u") and G.is_multigraph() and parallel_edges:
-        chain = itertools.chain.from_iterable
-
-
-
-
-
-
-        triples = chain(((u, v, 1) for d in range(w)) for (u, v, w) in triples)
-
-
-
-
-
-
-
-
-    if G.is_multigraph() and not G.is_directed():
-        triples = ((u, v, d) for u, v, d in triples if u <= v)
-    G.add_weighted_edges_from(triples, weight=edge_attribute)
-    return G
+    warnings.warn(
+        (
+            "\n\nThe scipy.sparse array containers will be used instead of matrices\n"
+            "in Networkx 3.0. Use `from_scipy_sparse_array` instead."
+        ),
+        DeprecationWarning,
+        stacklevel=2,
+    )
+    return from_scipy_sparse_array(
+        A,
+        parallel_edges=parallel_edges,
+        create_using=create_using,
+        edge_attribute=edge_attribute,
+    )
```

```json
{
  "old_file": "networkx.convert_matrix.from_scipy_sparse_matrix/Vi-1_networkx-2.6.3.py",
  "new_file": "networkx.convert_matrix.from_scipy_sparse_matrix/Vi_networkx-2.7.py",
  "lines_added": 14,
  "lines_removed": 35
}
```
