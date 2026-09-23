# 一、突变情况分析

- **Total**: 55
- **替代API**: `networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance`
- **10% 阈值**: 5.5

## Vi-1 (networkx-1.4-networkx-2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 3 | 0.4462 |
| tokenBased | 11 | 0.3973 |
| treeBased | 15 | 0.3614 |

## Vi (networkx-1.5-networkx-2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.5876 |
| tokenBased | 2 | 0.5542 |
| treeBased | 2 | 0.4532 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 3 | 1 | +2 | false |
| tokenBased | 11 | 2 | +9 | true |
| treeBased | 15 | 2 | +13 | true |

```json
{
  "total": 55,
  "replacement_api": "networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance",
  "threshold_10pct": 5.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 3,
      "score": 0.446206
    },
    "tokenBased": {
      "rank": 11,
      "score": 0.397321
    },
    "treeBased": {
      "rank": 15,
      "score": 0.361446
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1,
      "score": 0.58759
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.554217
    },
    "treeBased": {
      "rank": 2,
      "score": 0.453237
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 3,
      "vi_rank": 1,
      "delta": 2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 11,
      "vi_rank": 2,
      "delta": 9,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 15,
      "vi_rank": 2,
      "delta": 13,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.4.py`
- **new**: `networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-1.5.py`
- **+21 / -30**

```diff
--- networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.4.py
+++ networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-1.5.py
@@ -1,43 +1,34 @@
 def bellman_ford(G, source, weight = 'weight'):
     
-
-    if not G.is_directed():
-        directed = False
-    else:
-        directed = True
+    if source not in G:
+        raise KeyError("Node %s is not found in the graph"%source)
+    numb_nodes = len(G)
 
     dist = {source: 0}
     pred = {source: None}
 
-    if G.number_of_nodes() == 1:
+    if numb_nodes == 1:
        return pred, dist
     
-    def process_edge(u, v, weight):
+    if G.is_multigraph():
+        def get_weight(edge_dict):
+            return min([eattr.get(weight,1) for eattr in edge_dict.values()])
+    else:
+        def get_weight(edge_dict):
+            return edge_dict.get(weight,1)
 
-        if dist.get(u) is not None:
-            if dist.get(v) is None or dist[v] > dist[u] + weight:
-                dist[v] = dist[u] + weight
-                pred[v] = u
-                return False
-        return True
+    for i in range(numb_nodes):
+        no_changes=True
 
-    for i in range(G.number_of_nodes()):
-        feasible = True
-        for u, v in G.edges():
-            if G.is_multigraph():
-                edata = min([eattr.get(weight, 1)
-                             for eattr in G[u][v].values()])
-            else:
-                edata = G[u][v].get(weight, 1)
-            if not process_edge(u, v, edata):
-                feasible = False
-            if not directed:
-                if not (v, u) in G.edges():
-                    if not process_edge(v, u, edata):
-                        feasible = False
-        if feasible:
+        for u, dist_u in list(dist.items()):
+            for v, edict in G[u].items():
+                dist_v = dist_u + get_weight(edict)
+                if v not in dist or dist[v] > dist_v:
+                    dist[v] = dist_v
+                    pred[v] = u
+                    no_changes = False
+        if no_changes:
             break
-
-    if i + 1 == G.number_of_nodes():
+    else:
         raise nx.NetworkXUnbounded("Negative cost cycle detected.")
     return pred, dist
```

```json
{
  "old_file": "networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.4.py",
  "new_file": "networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-1.5.py",
  "lines_added": 21,
  "lines_removed": 30
}
```
