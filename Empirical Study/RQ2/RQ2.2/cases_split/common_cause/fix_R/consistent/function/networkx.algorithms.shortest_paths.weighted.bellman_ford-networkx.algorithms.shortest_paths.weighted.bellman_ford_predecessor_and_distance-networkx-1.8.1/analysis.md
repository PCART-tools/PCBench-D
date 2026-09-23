# 一、突变情况分析

- **Total**: 55
- **替代API**: `networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance`
- **10% 阈值**: 5.5

## Vi-1 (networkx-1.8.1-networkx-2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.5876 |
| tokenBased | 2 | 0.5542 |
| treeBased | 2 | 0.4532 |

## Vi (networkx-1.9-networkx-2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 3 | 0.4272 |
| tokenBased | 11 | 0.3789 |
| treeBased | 9 | 0.4005 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 3 | -2 | false |
| tokenBased | 2 | 11 | -9 | true |
| treeBased | 2 | 9 | -7 | true |

```json
{
  "total": 55,
  "replacement_api": "networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance",
  "threshold_10pct": 5.5,
  "vi_minus_1": {
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
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 3,
      "delta": -2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2,
      "vi_rank": 11,
      "delta": -9,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2,
      "vi_rank": 9,
      "delta": -7,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.8.1.py`
- **new**: `networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-1.9.py`
- **+39 / -18**

```diff
--- networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.8.1.py
+++ networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-1.9.py
@@ -1,34 +1,55 @@
-def bellman_ford(G, source, weight = 'weight'):
+def bellman_ford(G, source, weight='weight'):
     
     if source not in G:
-        raise KeyError("Node %s is not found in the graph"%source)
-    numb_nodes = len(G)
+        raise KeyError("Node %s is not found in the graph" % source)
+
+    for u, v, attr in G.selfloop_edges(data=True):
+        if attr.get(weight, 1) < 0:
+            raise nx.NetworkXUnbounded("Negative cost cycle detected.")
 
     dist = {source: 0}
     pred = {source: None}
 
-    if numb_nodes == 1:
-       return pred, dist
+    if len(G) == 1:
+        return pred, dist
 
     if G.is_multigraph():
         def get_weight(edge_dict):
-            return min([eattr.get(weight,1) for eattr in edge_dict.values()])
+            return min(eattr.get(weight, 1) for eattr in edge_dict.values())
     else:
         def get_weight(edge_dict):
-            return edge_dict.get(weight,1)
+            return edge_dict.get(weight, 1)
 
-    for i in range(numb_nodes):
-        no_changes=True
+    if G.is_directed():
+        G_succ = G.succ
+    else:
+        G_succ = G.adj
 
-        for u, dist_u in list(dist.items()):
-            for v, edict in G[u].items():
-                dist_v = dist_u + get_weight(edict)
-                if v not in dist or dist[v] > dist_v:
+    inf = float('inf')
+    n = len(G)
+
+    count = {}
+    q = deque([source])
+    in_q = set([source])
+
+    while q:
+        u = q.popleft()
+        in_q.remove(u)
+
+        if pred[u] not in in_q:
+            dist_u = dist[u]
+            for v, e in G_succ[u].items():
+                dist_v = dist_u + get_weight(e)
+                if dist_v < dist.get(v, inf):
+                    if v not in in_q:
+                        q.append(v)
+                        in_q.add(v)
+                        count_v = count.get(v, 0) + 1
+                        if count_v == n:
+                            raise nx.NetworkXUnbounded(
+                                "Negative cost cycle detected.")
+                        count[v] = count_v
                     dist[v] = dist_v
                     pred[v] = u
-                    no_changes = False
-        if no_changes:
-            break
-    else:
-        raise nx.NetworkXUnbounded("Negative cost cycle detected.")
+
     return pred, dist
```

```json
{
  "old_file": "networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.8.1.py",
  "new_file": "networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-1.9.py",
  "lines_added": 39,
  "lines_removed": 18
}
```
