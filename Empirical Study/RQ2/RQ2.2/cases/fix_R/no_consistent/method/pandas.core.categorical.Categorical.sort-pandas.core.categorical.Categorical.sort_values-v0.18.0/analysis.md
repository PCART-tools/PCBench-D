# 一、突变情况分析

- **Total**: 2513
- **替代API**: `pandas.core.categorical.Categorical.sort_values`
- **10% 阈值**: 251.3

## Vi-1 (v0.18.0-v0.21.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2205 | 0.2418 |
| tokenBased | 2090 | 0.1275 |
| treeBased | 2195 | 0.2154 |

## Vi (v0.18.1-v0.21.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2141 | 0.2940 |
| tokenBased | 1801 | 0.1883 |
| treeBased | 2215 | 0.2762 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2205 | 2141 | +64 | false |
| tokenBased | 2090 | 1801 | +289 | true |
| treeBased | 2195 | 2215 | -20 | false |

```json
{
  "total": 2513,
  "replacement_api": "pandas.core.categorical.Categorical.sort_values",
  "threshold_10pct": 251.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2205,
      "score": 0.241818
    },
    "tokenBased": {
      "rank": 2090,
      "score": 0.127517
    },
    "treeBased": {
      "rank": 2195,
      "score": 0.215385
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2141,
      "score": 0.293991
    },
    "tokenBased": {
      "rank": 1801,
      "score": 0.188312
    },
    "treeBased": {
      "rank": 2215,
      "score": 0.27619
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2205,
      "vi_rank": 2141,
      "delta": 64,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2090,
      "vi_rank": 1801,
      "delta": 289,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2195,
      "vi_rank": 2215,
      "delta": -20,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.categorical.Categorical.sort/Vi-1_v0.18.0.py`
- **new**: `pandas.core.categorical.Categorical.sort/Vi_v0.18.1.py`
- **+4 / -1**

```diff
--- pandas.core.categorical.Categorical.sort/Vi-1_v0.18.0.py
+++ pandas.core.categorical.Categorical.sort/Vi_v0.18.1.py
@@ -1,4 +1,7 @@
-    def sort(self, inplace=True, ascending=True, na_position='last'):
+    def sort(self, inplace=True, ascending=True, na_position='last', **kwargs):
         
+        warn("sort is deprecated, use sort_values(...)", FutureWarning,
+             stacklevel=2)
+        nv.validate_sort(tuple(), kwargs)
         return self.sort_values(inplace=inplace, ascending=ascending,
                                 na_position=na_position)
```

```json
{
  "old_file": "pandas.core.categorical.Categorical.sort/Vi-1_v0.18.0.py",
  "new_file": "pandas.core.categorical.Categorical.sort/Vi_v0.18.1.py",
  "lines_added": 4,
  "lines_removed": 1
}
```
