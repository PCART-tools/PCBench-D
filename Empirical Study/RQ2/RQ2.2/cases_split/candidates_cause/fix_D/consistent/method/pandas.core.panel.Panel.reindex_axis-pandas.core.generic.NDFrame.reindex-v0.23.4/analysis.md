# 一、突变情况分析

- **Total**: 2609
- **替代API**: `pandas.core.generic.NDFrame.reindex`
- **10% 阈值**: 260.9

## Vi-1 (v0.20.3-v0.23.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2429 | 0.1616 |
| tokenBased | 1770 | 0.1726 |
| treeBased | 2376 | 0.2489 |

## Vi (v0.20.3-v0.24.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2721 | 0.1594 |
| tokenBased | 1990 | 0.1667 |
| treeBased | 2488 | 0.2679 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2429 | 2721 | -292 | true |
| tokenBased | 1770 | 1990 | -220 | false |
| treeBased | 2376 | 2488 | -112 | false |

```json
{
  "total": 2609,
  "replacement_api": "pandas.core.generic.NDFrame.reindex",
  "threshold_10pct": 260.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2429,
      "score": 0.161633
    },
    "tokenBased": {
      "rank": 1770,
      "score": 0.172619
    },
    "treeBased": {
      "rank": 2376,
      "score": 0.248889
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2721,
      "score": 0.15942
    },
    "tokenBased": {
      "rank": 1990,
      "score": 0.166667
    },
    "treeBased": {
      "rank": 2488,
      "score": 0.267943
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2429,
      "vi_rank": 2721,
      "delta": -292,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1770,
      "vi_rank": 1990,
      "delta": -220,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2376,
      "vi_rank": 2488,
      "delta": -112,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.23.4/pandas.core.generic.NDFrame.reindex.py`
- **new**: `R_candidates/Vi_v0.24.0/pandas.core.generic.NDFrame.reindex.py`
- **+3 / -3**

```diff
--- R_candidates/Vi-1_v0.23.4/pandas.core.generic.NDFrame.reindex.py
+++ R_candidates/Vi_v0.24.0/pandas.core.generic.NDFrame.reindex.py
@@ -1,7 +1,7 @@
-    @Appender(_shared_docs['reindex'] % dict(axes="axes", klass="NDFrame",
-                                             optional_labels="",
-                                             optional_axis=""))
     def reindex(self, *args, **kwargs):
+        
+
+
 
 
         axes, kwargs = self._construct_axes_from_arguments(args, kwargs)
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.23.4/pandas.core.generic.NDFrame.reindex.py",
  "new_file": "R_candidates/Vi_v0.24.0/pandas.core.generic.NDFrame.reindex.py",
  "lines_added": 3,
  "lines_removed": 3
}
```
