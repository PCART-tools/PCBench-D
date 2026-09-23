# Diff 分块分析：networkx.algorithms.shortest_paths.weighted.bellman_ford-networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance-networkx-1.8.1
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/networkx.algorithms.shortest_paths.weighted.bellman_ford-networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance-networkx-1.8.1/networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi-1_networkx-1.8.1.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/networkx.algorithms.shortest_paths.weighted.bellman_ford-networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance-networkx-1.8.1/networkx.algorithms.shortest_paths.weighted.bellman_ford/Vi_networkx-1.9.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/networkx.algorithms.shortest_paths.weighted.bellman_ford-networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance-networkx-1.8.1/R_candidates/networkx-2.1/networkx.algorithms.shortest_paths.weighted.bellman_ford_predecessor_and_distance.py
- 实验组：fix_R
- 总变更：+44 / -23 行
- 分块数：8

## Block 1 — block_001.patch
定位：@@ -1,2 +1,2 @@
说明：def bellman_ford(G, source, weight = 'weight'):、def bellman_ford(G, source, weight='weight'):

## Block 2 — block_002.patch
定位：@@ -39,6 +39,6 @@
说明：>>> pred、{0: None, 1: 0, 2: 1, 3: 2, 4: 3}、>>> dist...

## Block 3 — block_003.patch
定位：@@ -63,4 +63,7 @@
说明：raise KeyError("Node %s is not found in the graph"%source)、numb_nodes = len(G)、raise KeyError("Node %s is not found in the graph" % source)...

## Block 4 — block_004.patch
定位：@@ -69,4 +72,4 @@
说明：if numb_nodes == 1:、return pred, dist、if len(G) == 1:...

## Block 5 — block_005.patch
定位：@@ -74,3 +77,3 @@
说明：return min([eattr.get(weight,1) for eattr in edge_dict.value、return min(eattr.get(weight, 1) for eattr in edge_dict.value

## Block 6 — block_006.patch
定位：@@ -77,3 +80,3 @@
说明：return edge_dict.get(weight,1)、return edge_dict.get(weight, 1)

## Block 7 — block_007.patch
定位：@@ -79,9 +82,31 @@
说明：for i in range(numb_nodes):、no_changes=True、# Only need edges from nodes in dist b/c all others have dis...

## Block 8 — block_008.patch
定位：@@ -88,7 +113,3 @@
说明：no_changes = False、if no_changes:、break...
