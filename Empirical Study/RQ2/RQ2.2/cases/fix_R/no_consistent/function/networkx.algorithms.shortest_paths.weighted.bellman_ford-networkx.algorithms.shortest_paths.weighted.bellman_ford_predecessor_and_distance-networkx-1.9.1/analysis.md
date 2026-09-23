# 一、突变情况分析

- **Total**: 55
- **替代API**: `networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance`
- **10% 阈值**: 5.5

## Vi-1 (networkx-1.9.1-networkx-2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 3 | 0.4272 |
| tokenBased | 11 | 0.3789 |
| treeBased | 9 | 0.4005 |

## Vi (networkx-1.10-networkx-2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 5 | 0.6019 |
| tokenBased | 1 | 0.6522 |
| treeBased | 1 | 0.6582 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 3 | 5 | -2 | false |
| tokenBased | 11 | 1 | +10 | true |
| treeBased | 9 | 1 | +8 | true |

```json
{
  "total": 55,
  "replacement_api": "networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance",
  "threshold_10pct": 5.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 3,
      "score": 0.427225
    },
    "tokenBased": {
      "rank": 11,
      "score": 0.378906
    },
    "treeBased": {
      "rank": 9,
      "score": 0.400538
    }
  },
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 3,
      "vi_rank": 5,
      "delta": -2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 11,
      "vi_rank": 1,
      "delta": 10,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 9,
      "vi_rank": 1,
      "delta": 8,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.9.1.py`
- **new**: `networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-1.10.py`
- **+1 / -40**

```diff
--- networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.9.1.py
+++ networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-1.10.py
@@ -13,43 +13,4 @@
     if len(G) == 1:
         return pred, dist
 
-    if G.is_multigraph():
-        def get_weight(edge_dict):
-            return min(eattr.get(weight, 1) for eattr in edge_dict.values())
-    else:
-        def get_weight(edge_dict):
-            return edge_dict.get(weight, 1)
-
-    if G.is_directed():
-        G_succ = G.succ
-    else:
-        G_succ = G.adj
-
-    inf = float('inf')
-    n = len(G)
-
-    count = {}
-    q = deque([source])
-    in_q = set([source])
-
-    while q:
-        u = q.popleft()
-        in_q.remove(u)
-
-        if pred[u] not in in_q:
-            dist_u = dist[u]
-            for v, e in G_succ[u].items():
-                dist_v = dist_u + get_weight(e)
-                if dist_v < dist.get(v, inf):
-                    if v not in in_q:
-                        q.append(v)
-                        in_q.add(v)
-                        count_v = count.get(v, 0) + 1
-                        if count_v == n:
-                            raise nx.NetworkXUnbounded(
-                                "Negative cost cycle detected.")
-                        count[v] = count_v
-                    dist[v] = dist_v
-                    pred[v] = u
-
-    return pred, dist
+    return _bellman_ford_relaxation(G, pred, dist, [source], weight)
```

```json
{
  "old_file": "networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.9.1.py",
  "new_file": "networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-1.10.py",
  "lines_added": 1,
  "lines_removed": 40
}
```
