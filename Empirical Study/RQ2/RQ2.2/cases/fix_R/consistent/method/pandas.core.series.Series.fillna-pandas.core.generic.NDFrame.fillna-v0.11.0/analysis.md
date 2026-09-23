# 一、突变情况分析

- **Total**: 1231
- **替代API**: `pandas.core.generic.NDFrame.fillna`
- **10% 阈值**: 123.1

## Vi-1 (v0.11.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 351 | 0.3267 |
| tokenBased | 355 | 0.3278 |
| treeBased | 273 | 0.4113 |

## Vi (v0.12.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 268 | 0.3333 |
| tokenBased | 205 | 0.3980 |
| treeBased | 49 | 0.4667 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 351 | 268 | +83 | false |
| tokenBased | 355 | 205 | +150 | true |
| treeBased | 273 | 49 | +224 | true |

```json
{
  "total": 1231,
  "replacement_api": "pandas.core.generic.NDFrame.fillna",
  "threshold_10pct": 123.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 351,
      "score": 0.326671
    },
    "tokenBased": {
      "rank": 355,
      "score": 0.327759
    },
    "treeBased": {
      "rank": 273,
      "score": 0.411255
    }
  },
  "vi": {
    "mapBased": {
      "rank": 268,
      "score": 0.333256
    },
    "tokenBased": {
      "rank": 205,
      "score": 0.397993
    },
    "treeBased": {
      "rank": 49,
      "score": 0.466667
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 351,
      "vi_rank": 268,
      "delta": 83,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 355,
      "vi_rank": 205,
      "delta": 150,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 273,
      "vi_rank": 49,
      "delta": 224,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.series.Series.fillna/Vi-1_v0.11.0.py`
- **new**: `pandas.core.series.Series.fillna/Vi_v0.12.0.py`
- **+3 / -0**

```diff
--- pandas.core.series.Series.fillna/Vi-1_v0.11.0.py
+++ pandas.core.series.Series.fillna/Vi_v0.12.0.py
@@ -2,6 +2,9 @@
     def fillna(self, value=None, method=None, inplace=False,
                limit=None):
         
+        if isinstance(value, (list, tuple)):
+            raise TypeError('"value" parameter must be a scalar or dict, but '
+                            'you passed a "{0}"'.format(type(value).__name__))
         if not self._can_hold_na:
             return self.copy() if not inplace else None
 
```

```json
{
  "old_file": "pandas.core.series.Series.fillna/Vi-1_v0.11.0.py",
  "new_file": "pandas.core.series.Series.fillna/Vi_v0.12.0.py",
  "lines_added": 3,
  "lines_removed": 0
}
```
