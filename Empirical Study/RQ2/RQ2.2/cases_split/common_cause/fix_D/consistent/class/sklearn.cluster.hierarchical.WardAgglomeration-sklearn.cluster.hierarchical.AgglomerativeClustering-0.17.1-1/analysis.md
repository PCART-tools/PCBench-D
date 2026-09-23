# 一、突变情况分析

- **Total**: 16
- **替代API**: `sklearn.cluster.hierarchical.AgglomerativeClustering`
- **10% 阈值**: 1.6

## Vi-1 (0.16.1-0.17.1-1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 8 | 0.1937 |
| tokenBased | 12 | 0.1122 |

## Vi (0.16.1-0.18)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 6 | 0.1982 |
| tokenBased | 10 | 0.1144 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 8 | 6 | +2 | true |
| tokenBased | 12 | 10 | +2 | true |

```json
{
  "total": 16,
  "replacement_api": "sklearn.cluster.hierarchical.AgglomerativeClustering",
  "threshold_10pct": 1.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 8,
      "score": 0.193731
    },
    "tokenBased": {
      "rank": 12,
      "score": 0.112179
    }
  },
  "vi": {
    "mapBased": {
      "rank": 6,
      "score": 0.198175
    },
    "tokenBased": {
      "rank": 10,
      "score": 0.114379
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 8,
      "vi_rank": 6,
      "delta": 2,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 12,
      "vi_rank": 10,
      "delta": 2,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.17.1-1/sklearn.cluster.hierarchical.AgglomerativeClustering.py`
- **new**: `R_candidates/Vi_0.18/sklearn.cluster.hierarchical.AgglomerativeClustering.py`
- **+2 / -5**

```diff
--- R_candidates/Vi-1_0.17.1-1/sklearn.cluster.hierarchical.AgglomerativeClustering.py
+++ R_candidates/Vi_0.18/sklearn.cluster.hierarchical.AgglomerativeClustering.py
@@ -3,12 +3,10 @@
 
     def __init__(self, n_clusters=2, affinity="euclidean",
                  memory=Memory(cachedir=None, verbose=0),
-                 connectivity=None, n_components=None,
-                 compute_full_tree='auto', linkage='ward',
-                 pooling_func=np.mean):
+                 connectivity=None, compute_full_tree='auto',
+                 linkage='ward', pooling_func=np.mean):
         self.n_clusters = n_clusters
         self.memory = memory
-        self.n_components = n_components
         self.connectivity = connectivity
         self.compute_full_tree = compute_full_tree
         self.linkage = linkage
@@ -64,7 +62,6 @@
             kwargs['affinity'] = self.affinity
         self.children_, self.n_components_, self.n_leaves_, parents = \
             memory.cache(tree_builder)(X, connectivity,
-                                       n_components=self.n_components,
                                        n_clusters=n_clusters,
                                        **kwargs)
 
```

```json
{
  "old_file": "R_candidates/Vi-1_0.17.1-1/sklearn.cluster.hierarchical.AgglomerativeClustering.py",
  "new_file": "R_candidates/Vi_0.18/sklearn.cluster.hierarchical.AgglomerativeClustering.py",
  "lines_added": 2,
  "lines_removed": 5
}
```
