# 一、突变情况分析

- **Total**: 401
- **替代API**: `pandas.core.reshape.get_dummies`
- **10% 阈值**: 40.1

## Vi-1 (v0.14.1-v0.18.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 316 | 0.2834 |
| tokenBased | 341 | 0.1652 |
| treeBased | 359 | 0.2276 |

## Vi (v0.14.1-v0.19.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 265 | 0.2834 |
| tokenBased | 277 | 0.1659 |
| treeBased | 297 | 0.2284 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 316 | 265 | +51 | true |
| tokenBased | 341 | 277 | +64 | true |
| treeBased | 359 | 297 | +62 | true |

```json
{
  "total": 401,
  "replacement_api": "pandas.core.reshape.get_dummies",
  "threshold_10pct": 40.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 316,
      "score": 0.283372
    },
    "tokenBased": {
      "rank": 341,
      "score": 0.165217
    },
    "treeBased": {
      "rank": 359,
      "score": 0.227586
    }
  },
  "vi": {
    "mapBased": {
      "rank": 265,
      "score": 0.283372
    },
    "tokenBased": {
      "rank": 277,
      "score": 0.165939
    },
    "treeBased": {
      "rank": 297,
      "score": 0.228374
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 316,
      "vi_rank": 265,
      "delta": 51,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 341,
      "vi_rank": 277,
      "delta": 64,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 359,
      "vi_rank": 297,
      "delta": 62,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.18.1/pandas.core.reshape.get_dummies.py`
- **new**: `R_candidates/Vi_v0.19.0/pandas.core.reshape.get_dummies.py`
- **+1 / -1**

```diff
--- R_candidates/Vi-1_v0.18.1/pandas.core.reshape.get_dummies.py
+++ R_candidates/Vi_v0.19.0/pandas.core.reshape.get_dummies.py
@@ -18,7 +18,7 @@
             length_msg = ("Length of '{0}' ({1}) did not match the length of "
                           "the columns being encoded ({2}).")
 
-            if com.is_list_like(item):
+            if is_list_like(item):
                 if not len(item) == len(columns_to_encode):
                     raise ValueError(length_msg.format(name, len(item),
                                                        len(columns_to_encode)))
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.18.1/pandas.core.reshape.get_dummies.py",
  "new_file": "R_candidates/Vi_v0.19.0/pandas.core.reshape.get_dummies.py",
  "lines_added": 1,
  "lines_removed": 1
}
```
