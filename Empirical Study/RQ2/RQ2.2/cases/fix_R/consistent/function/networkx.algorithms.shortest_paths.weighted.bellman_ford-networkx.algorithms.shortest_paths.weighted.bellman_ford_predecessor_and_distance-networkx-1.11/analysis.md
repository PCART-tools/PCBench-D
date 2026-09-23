# 一、突变情况分析

- **Total**: 55
- **替代API**: `networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance`
- **10% 阈值**: 5.5

## Vi-1 (networkx-1.11-networkx-2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 5 | 0.6019 |
| tokenBased | 1 | 0.6522 |
| treeBased | 1 | 0.6582 |

## Vi (networkx-2.0-networkx-2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 38 | 0.3443 |
| tokenBased | 33 | 0.2411 |
| treeBased | 40 | 0.2908 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 5 | 38 | -33 | true |
| tokenBased | 1 | 33 | -32 | true |
| treeBased | 1 | 40 | -39 | true |

```json
{
  "total": 55,
  "replacement_api": "networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance",
  "threshold_10pct": 5.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 5,
      "score": 0.601878
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.652174
    },
    "treeBased": {
      "rank": 1,
      "score": 0.658163
    }
  },
  "vi": {
    "mapBased": {
      "rank": 38,
      "score": 0.344282
    },
    "tokenBased": {
      "rank": 33,
      "score": 0.241071
    },
    "treeBased": {
      "rank": 40,
      "score": 0.29078
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 5,
      "vi_rank": 38,
      "delta": -33,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 33,
      "delta": -32,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 40,
      "delta": -39,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.11.py`
- **new**: `networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-2.0.py`
- **+4 / -13**

```diff
--- networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.11.py
+++ networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-2.0.py
@@ -1,16 +1,7 @@
 def bellman_ford(G, source, weight='weight'):
     
-    if source not in G:
-        raise KeyError("Node %s is not found in the graph" % source)
+    msg = "Function bellman_ford() is deprecated and will be removed" \
+        "in 2.1, use bellman_ford_predecessor_and_distance() instead."
+    _warnings.warn(msg, DeprecationWarning)
 
-    for u, v, attr in G.selfloop_edges(data=True):
-        if attr.get(weight, 1) < 0:
-            raise nx.NetworkXUnbounded("Negative cost cycle detected.")
-
-    dist = {source: 0}
-    pred = {source: None}
-
-    if len(G) == 1:
-        return pred, dist
-
-    return _bellman_ford_relaxation(G, pred, dist, [source], weight)
+    return bellman_ford_predecessor_and_distance(G, source, weight=weight)
```

```json
{
  "old_file": "networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.11.py",
  "new_file": "networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-2.0.py",
  "lines_added": 4,
  "lines_removed": 13
}
```
