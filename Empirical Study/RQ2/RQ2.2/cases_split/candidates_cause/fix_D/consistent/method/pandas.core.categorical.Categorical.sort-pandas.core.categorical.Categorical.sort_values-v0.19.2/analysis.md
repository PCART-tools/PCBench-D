# 一、突变情况分析

- **Total**: 1332
- **替代API**: `pandas.core.categorical.Categorical.sort_values`
- **10% 阈值**: 133.2

## Vi-1 (v0.18.0-v0.19.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1143 | 0.2603 |
| tokenBased | 1086 | 0.1367 |
| treeBased | 1145 | 0.2270 |

## Vi (v0.18.0-v0.20.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2144 | 0.2474 |
| tokenBased | 2031 | 0.1301 |
| treeBased | 2143 | 0.2199 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1143 | 2144 | -1001 | true |
| tokenBased | 1086 | 2031 | -945 | true |
| treeBased | 1145 | 2143 | -998 | true |

```json
{
  "total": 1332,
  "replacement_api": "pandas.core.categorical.Categorical.sort_values",
  "threshold_10pct": 133.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1143,
      "score": 0.260274
    },
    "tokenBased": {
      "rank": 1086,
      "score": 0.136691
    },
    "treeBased": {
      "rank": 1145,
      "score": 0.227027
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2144,
      "score": 0.247442
    },
    "tokenBased": {
      "rank": 2031,
      "score": 0.130137
    },
    "treeBased": {
      "rank": 2143,
      "score": 0.219895
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1143,
      "vi_rank": 2144,
      "delta": -1001,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1086,
      "vi_rank": 2031,
      "delta": -945,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1145,
      "vi_rank": 2143,
      "delta": -998,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.19.2/pandas.core.categorical.Categorical.sort_values.py`
- **new**: `R_candidates/Vi_v0.20.0/pandas.core.categorical.Categorical.sort_values.py`
- **+1 / -0**

```diff
--- R_candidates/Vi-1_v0.19.2/pandas.core.categorical.Categorical.sort_values.py
+++ R_candidates/Vi_v0.20.0/pandas.core.categorical.Categorical.sort_values.py
@@ -1,5 +1,6 @@
     def sort_values(self, inplace=False, ascending=True, na_position='last'):
         
+        inplace = validate_bool_kwarg(inplace, 'inplace')
         if na_position not in ['last', 'first']:
             raise ValueError('invalid na_position: {!r}'.format(na_position))
 
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.19.2/pandas.core.categorical.Categorical.sort_values.py",
  "new_file": "R_candidates/Vi_v0.20.0/pandas.core.categorical.Categorical.sort_values.py",
  "lines_added": 1,
  "lines_removed": 0
}
```
