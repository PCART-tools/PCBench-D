# 一、突变情况分析

- **Total**: 2850
- **替代API**: `pandas.core.series.Series.reindex`
- **10% 阈值**: 285.0

## Vi-1 (v0.20.3-v0.25.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 276 | 0.6728 |
| tokenBased | 4 | 0.4706 |
| treeBased | 121 | 0.6034 |

## Vi (v0.21.0-v0.25.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 622 | 0.5908 |
| tokenBased | 122 | 0.3953 |
| treeBased | 322 | 0.5217 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 276 | 622 | -346 | true |
| tokenBased | 4 | 122 | -118 | false |
| treeBased | 121 | 322 | -201 | false |

```json
{
  "total": 2850,
  "replacement_api": "pandas.core.series.Series.reindex",
  "threshold_10pct": 285.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 276,
      "score": 0.67284
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.470588
    },
    "treeBased": {
      "rank": 121,
      "score": 0.603448
    }
  },
  "vi": {
    "mapBased": {
      "rank": 622,
      "score": 0.590786
    },
    "tokenBased": {
      "rank": 122,
      "score": 0.395349
    },
    "treeBased": {
      "rank": 322,
      "score": 0.521739
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 276,
      "vi_rank": 622,
      "delta": -346,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 4,
      "vi_rank": 122,
      "delta": -118,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 121,
      "vi_rank": 322,
      "delta": -201,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.series.Series.reindex_axis/Vi-1_v0.20.3.py`
- **new**: `pandas.core.series.Series.reindex_axis/Vi_v0.21.0.py`
- **+4 / -0**

```diff
--- pandas.core.series.Series.reindex_axis/Vi-1_v0.20.3.py
+++ pandas.core.series.Series.reindex_axis/Vi_v0.21.0.py
@@ -2,4 +2,8 @@
         
         if axis != 0:
             raise ValueError("cannot reindex series on non-zero axis!")
+        msg = ("'.reindex_axis' is deprecated and will be removed in a future "
+               "version. Use '.reindex' instead.")
+        warnings.warn(msg, FutureWarning, stacklevel=2)
+
         return self.reindex(index=labels, **kwargs)
```

```json
{
  "old_file": "pandas.core.series.Series.reindex_axis/Vi-1_v0.20.3.py",
  "new_file": "pandas.core.series.Series.reindex_axis/Vi_v0.21.0.py",
  "lines_added": 4,
  "lines_removed": 0
}
```
