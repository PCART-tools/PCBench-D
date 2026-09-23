# 一、突变情况分析

- **Total**: 215
- **替代API**: `scipy.optimize._basinhopping.basinhopping`
- **10% 阈值**: 21.5

## Vi-1 (v0.13.3-v0.16.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 90 | 0.2517 |
| tokenBased | 71 | 0.2305 |
| treeBased | 25 | 0.3959 |

## Vi (v0.13.3-v0.17.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 137 | 0.2517 |
| tokenBased | 118 | 0.2219 |
| treeBased | 32 | 0.3927 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 90 | 137 | -47 | true |
| tokenBased | 71 | 118 | -47 | true |
| treeBased | 25 | 32 | -7 | false |

```json
{
  "total": 215,
  "replacement_api": "scipy.optimize._basinhopping.basinhopping",
  "threshold_10pct": 21.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 90,
      "score": 0.251723
    },
    "tokenBased": {
      "rank": 71,
      "score": 0.230519
    },
    "treeBased": {
      "rank": 25,
      "score": 0.395881
    }
  },
  "vi": {
    "mapBased": {
      "rank": 137,
      "score": 0.251723
    },
    "tokenBased": {
      "rank": 118,
      "score": 0.221865
    },
    "treeBased": {
      "rank": 32,
      "score": 0.392694
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 90,
      "vi_rank": 137,
      "delta": -47,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 71,
      "vi_rank": 118,
      "delta": -47,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 25,
      "vi_rank": 32,
      "delta": -7,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.16.1/scipy.optimize._basinhopping.basinhopping.py`
- **new**: `R_candidates/Vi_v0.17.0/scipy.optimize._basinhopping.basinhopping.py`
- **+3 / -3**

```diff
--- R_candidates/Vi-1_v0.16.1/scipy.optimize._basinhopping.basinhopping.py
+++ R_candidates/Vi_v0.17.0/scipy.optimize._basinhopping.basinhopping.py
@@ -68,10 +68,10 @@
             break
 
 
-    lowest = bh.storage.get_lowest()
     res = bh.res
-    res.x = np.copy(lowest[0])
-    res.fun = lowest[1]
+    res.lowest_optimization_result = bh.storage.get_lowest()
+    res.x = np.copy(res.lowest_optimization_result.x)
+    res.fun = res.lowest_optimization_result.fun
     res.message = message
     res.nit = i + 1
     return res
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.16.1/scipy.optimize._basinhopping.basinhopping.py",
  "new_file": "R_candidates/Vi_v0.17.0/scipy.optimize._basinhopping.basinhopping.py",
  "lines_added": 3,
  "lines_removed": 3
}
```
