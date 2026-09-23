# 一、突变情况分析

- **Total**: 95
- **替代API**: `networkx.algorithms.tree.operations.join_trees`
- **10% 阈值**: 9.5

## Vi-1 (networkx-3.1-networkx-3.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.6030 |
| tokenBased | 1 | 0.6633 |
| treeBased | 1 | 0.5738 |

## Vi (networkx-3.2-networkx-3.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 59 | 0.2153 |
| tokenBased | 73 | 0.1233 |
| treeBased | 76 | 0.2000 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 59 | -58 | true |
| tokenBased | 1 | 73 | -72 | true |
| treeBased | 1 | 76 | -75 | true |

```json
{
  "total": 95,
  "replacement_api": "networkx.algorithms.tree.operations.join_trees",
  "threshold_10pct": 9.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.602972
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.663265
    },
    "treeBased": {
      "rank": 1,
      "score": 0.573816
    }
  },
  "vi": {
    "mapBased": {
      "rank": 59,
      "score": 0.215323
    },
    "tokenBased": {
      "rank": 73,
      "score": 0.123288
    },
    "treeBased": {
      "rank": 76,
      "score": 0.2
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 59,
      "delta": -58,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 73,
      "delta": -72,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 76,
      "delta": -75,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `networkx.algorithms.tree.operations.join/Vi-1_networkx-3.1.py`
- **new**: `networkx.algorithms.tree.operations.join/Vi_networkx-3.2.py`
- **+8 / -49**

```diff
--- networkx.algorithms.tree.operations.join/Vi-1_networkx-3.1.py
+++ networkx.algorithms.tree.operations.join/Vi_networkx-3.2.py
@@ -1,53 +1,12 @@
 def join(rooted_trees, label_attribute=None):
     
-    if len(rooted_trees) == 0:
-        return nx.empty_graph(1)
+    import warnings
 
+    warnings.warn(
+        "The function `join` is deprecated and is renamed `join_trees`.\n"
+        "The ``join`` function itself will be removed in v3.4",
+        DeprecationWarning,
+        stacklevel=2,
+    )
 
-    trees, roots = zip(*rooted_trees)
-
-
-
-    R = type(trees[0])()
-
-
-    if label_attribute is None:
-        label_attribute = "_old"
-    relabel = partial(
-        nx.convert_node_labels_to_integers, label_attribute=label_attribute
-    )
-    lengths = (len(tree) for tree in trees[:-1])
-    first_labels = chain([0], accumulate(lengths))
-    trees = [
-        relabel(tree, first_label=first_label + 1)
-        for tree, first_label in zip(trees, first_labels)
-    ]
-
-
-    roots = [
-        next(v for v, d in tree.nodes(data=True) if d.get("_old") == root)
-        for tree, root in zip(trees, roots)
-    ]
-
-
-    for tree in trees:
-        for v in tree:
-            tree.nodes[v].pop("_old")
-
-
-    nodes = (tree.nodes(data=True) for tree in trees)
-    edges = (tree.edges(data=True) for tree in trees)
-    R.add_nodes_from(chain.from_iterable(nodes))
-    R.add_edges_from(chain.from_iterable(edges))
-
-
-
-    for tree in trees:
-        R.graph.update(tree.graph)
-
-
-
-    R.add_node(0)
-    R.add_edges_from((0, root) for root in roots)
-
-    return R
+    return join_trees(rooted_trees, label_attribute=label_attribute)
```

```json
{
  "old_file": "networkx.algorithms.tree.operations.join/Vi-1_networkx-3.1.py",
  "new_file": "networkx.algorithms.tree.operations.join/Vi_networkx-3.2.py",
  "lines_added": 8,
  "lines_removed": 49
}
```
