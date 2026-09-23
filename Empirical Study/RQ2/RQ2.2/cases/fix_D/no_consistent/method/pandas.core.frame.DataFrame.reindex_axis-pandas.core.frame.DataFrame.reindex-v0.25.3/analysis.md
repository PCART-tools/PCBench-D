# 一、突变情况分析

- **Total**: 2853
- **替代API**: `pandas.core.frame.DataFrame.reindex`
- **10% 阈值**: 285.3

## Vi-1 (v0.20.3-v0.25.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1237 | 0.4192 |
| tokenBased | 51 | 0.4426 |
| treeBased | 444 | 0.4173 |

## Vi (v0.20.3-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 883 | 0.4432 |
| tokenBased | 81 | 0.3971 |
| treeBased | 432 | 0.4122 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1237 | 883 | +354 | true |
| tokenBased | 51 | 81 | -30 | false |
| treeBased | 444 | 432 | +12 | false |

```json
{
  "total": 2853,
  "replacement_api": "pandas.core.frame.DataFrame.reindex",
  "threshold_10pct": 285.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1237,
      "score": 0.419231
    },
    "tokenBased": {
      "rank": 51,
      "score": 0.442623
    },
    "treeBased": {
      "rank": 444,
      "score": 0.417323
    }
  },
  "vi": {
    "mapBased": {
      "rank": 883,
      "score": 0.443182
    },
    "tokenBased": {
      "rank": 81,
      "score": 0.397059
    },
    "treeBased": {
      "rank": 432,
      "score": 0.412214
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1237,
      "vi_rank": 883,
      "delta": 354,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 51,
      "vi_rank": 81,
      "delta": -30,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 444,
      "vi_rank": 432,
      "delta": 12,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.25.3/pandas.core.frame.DataFrame.reindex.py`
- **new**: `R_candidates/Vi_v1.0.0/pandas.core.frame.DataFrame.reindex.py`
- **+2 / -2**

```diff
--- R_candidates/Vi-1_v0.25.3/pandas.core.frame.DataFrame.reindex.py
+++ R_candidates/Vi_v1.0.0/pandas.core.frame.DataFrame.reindex.py
@@ -11,10 +11,10 @@
             ("tolerance", None),
         ],
     )
-    def reindex(self, *args, **kwargs):
+    def reindex(self, *args, **kwargs) -> "DataFrame":
         axes = validate_axis_style_args(self, args, kwargs, "labels", "reindex")
         kwargs.update(axes)
 
         kwargs.pop("axis", None)
         kwargs.pop("labels", None)
-        return super().reindex(**kwargs)
+        return self._ensure_type(super().reindex(**kwargs))
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.25.3/pandas.core.frame.DataFrame.reindex.py",
  "new_file": "R_candidates/Vi_v1.0.0/pandas.core.frame.DataFrame.reindex.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
