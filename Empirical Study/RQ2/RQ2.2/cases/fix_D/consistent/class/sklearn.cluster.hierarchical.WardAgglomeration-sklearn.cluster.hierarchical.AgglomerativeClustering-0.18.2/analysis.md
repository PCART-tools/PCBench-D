# 一、突变情况分析

- **Total**: 16
- **替代API**: `sklearn.cluster.hierarchical.AgglomerativeClustering`
- **10% 阈值**: 1.6

## Vi-1 (0.16.1-0.18.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 6 | 0.1982 |
| tokenBased | 10 | 0.1144 |

## Vi (0.16.1-0.19.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 8 | 0.1944 |
| tokenBased | 12 | 0.1054 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 6 | 8 | -2 | true |
| tokenBased | 10 | 12 | -2 | true |

```json
{
  "total": 16,
  "replacement_api": "sklearn.cluster.hierarchical.AgglomerativeClustering",
  "threshold_10pct": 1.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 6,
      "score": 0.198175
    },
    "tokenBased": {
      "rank": 10,
      "score": 0.114379
    }
  },
  "vi": {
    "mapBased": {
      "rank": 8,
      "score": 0.194388
    },
    "tokenBased": {
      "rank": 12,
      "score": 0.105422
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 6,
      "vi_rank": 8,
      "delta": -2,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 10,
      "vi_rank": 12,
      "delta": -2,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.18.2/sklearn.cluster.hierarchical.AgglomerativeClustering.py`
- **new**: `R_candidates/Vi_0.19.0/sklearn.cluster.hierarchical.AgglomerativeClustering.py`
- **+9 / -2**

```diff
--- R_candidates/Vi-1_0.18.2/sklearn.cluster.hierarchical.AgglomerativeClustering.py
+++ R_candidates/Vi_0.19.0/sklearn.cluster.hierarchical.AgglomerativeClustering.py
@@ -2,7 +2,7 @@
     
 
     def __init__(self, n_clusters=2, affinity="euclidean",
-                 memory=Memory(cachedir=None, verbose=0),
+                 memory=None,
                  connectivity=None, compute_full_tree='auto',
                  linkage='ward', pooling_func=np.mean):
         self.n_clusters = n_clusters
@@ -17,8 +17,15 @@
         
         X = check_array(X, ensure_min_samples=2, estimator=self)
         memory = self.memory
-        if isinstance(memory, six.string_types):
+        if memory is None:
+            memory = Memory(cachedir=None, verbose=0)
+        elif isinstance(memory, six.string_types):
             memory = Memory(cachedir=memory, verbose=0)
+        elif not isinstance(memory, Memory):
+            raise ValueError("'memory' should either be a string or"
+                             " a sklearn.externals.joblib.Memory"
+                             " instance, got 'memory={!r}' instead.".format(
+                                 type(memory)))
 
         if self.n_clusters <= 0:
             raise ValueError("n_clusters should be an integer greater than 0."
```

```json
{
  "old_file": "R_candidates/Vi-1_0.18.2/sklearn.cluster.hierarchical.AgglomerativeClustering.py",
  "new_file": "R_candidates/Vi_0.19.0/sklearn.cluster.hierarchical.AgglomerativeClustering.py",
  "lines_added": 9,
  "lines_removed": 2
}
```
