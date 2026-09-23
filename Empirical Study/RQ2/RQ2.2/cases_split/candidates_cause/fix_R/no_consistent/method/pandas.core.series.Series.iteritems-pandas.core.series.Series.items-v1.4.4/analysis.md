# 一、突变情况分析

- **Total**: 3391
- **替代API**: `pandas.core.series.Series.items`
- **10% 阈值**: 339.1

## Vi-1 (v1.4.4-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 379 | 0.8982 |
| tokenBased | 1 | 0.4688 |
| treeBased | 1 | 0.7273 |

## Vi (v1.5.0-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 9 | 0.9020 |
| tokenBased | 1 | 0.5128 |
| treeBased | 1 | 0.6731 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 379 | 9 | +370 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 1 | +0 | false |

```json
{
  "total": 3391,
  "replacement_api": "pandas.core.series.Series.items",
  "threshold_10pct": 339.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 379,
      "score": 0.898204
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.46875
    },
    "treeBased": {
      "rank": 1,
      "score": 0.727273
    }
  },
  "vi": {
    "mapBased": {
      "rank": 9,
      "score": 0.901961
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.512821
    },
    "treeBased": {
      "rank": 1,
      "score": 0.673077
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 379,
      "vi_rank": 9,
      "delta": 370,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.series.Series.iteritems/Vi-1_v1.4.4.py`
- **new**: `pandas.core.series.Series.iteritems/Vi_v1.5.0.py`
- **+7 / -1**

```diff
--- pandas.core.series.Series.iteritems/Vi-1_v1.4.4.py
+++ pandas.core.series.Series.iteritems/Vi_v1.5.0.py
@@ -1,3 +1,9 @@
-    @Appender(items.__doc__)
     def iteritems(self) -> Iterable[tuple[Hashable, Any]]:
+        
+        warnings.warn(
+            "iteritems is deprecated and will be removed in a future version. "
+            "Use .items instead.",
+            FutureWarning,
+            stacklevel=find_stack_level(inspect.currentframe()),
+        )
         return self.items()
```

```json
{
  "old_file": "pandas.core.series.Series.iteritems/Vi-1_v1.4.4.py",
  "new_file": "pandas.core.series.Series.iteritems/Vi_v1.5.0.py",
  "lines_added": 7,
  "lines_removed": 1
}
```
