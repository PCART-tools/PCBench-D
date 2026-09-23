# 一、突变情况分析

- **Total**: 567
- **替代API**: `jax._src.numpy.setops.isin`
- **10% 阈值**: 56.7

## Vi-1 (jax-v0.4.15-jax-v0.4.31)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 103 | 0.6620 |
| tokenBased | 1 | 0.6418 |
| treeBased | 2 | 0.6757 |

## Vi (jax-v0.4.15-jax-v0.4.32)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 231 | 0.5625 |
| tokenBased | 1 | 0.6143 |
| treeBased | 17 | 0.6203 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 103 | 231 | -128 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 2 | 17 | -15 | false |

```json
{
  "total": 567,
  "replacement_api": "jax._src.numpy.setops.isin",
  "threshold_10pct": 56.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 103,
      "score": 0.662037
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.641791
    },
    "treeBased": {
      "rank": 2,
      "score": 0.675676
    }
  },
  "vi": {
    "mapBased": {
      "rank": 231,
      "score": 0.5625
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.614286
    },
    "treeBased": {
      "rank": 17,
      "score": 0.620253
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 103,
      "vi_rank": 231,
      "delta": -128,
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
      "vi1_rank": 2,
      "vi_rank": 17,
      "delta": -15,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_jax-v0.4.31/jax._src.numpy.setops.isin.py`
- **new**: `R_candidates/Vi_jax-v0.4.32/jax._src.numpy.setops.isin.py`
- **+4 / -3**

```diff
--- R_candidates/Vi-1_jax-v0.4.31/jax._src.numpy.setops.isin.py
+++ R_candidates/Vi_jax-v0.4.32/jax._src.numpy.setops.isin.py
@@ -1,7 +1,8 @@
 def isin(element: ArrayLike, test_elements: ArrayLike,
-         assume_unique: bool = False, invert: bool = False) -> Array:
+         assume_unique: bool = False, invert: bool = False, *,
+         method='auto') -> Array:
   
-  del assume_unique
   check_arraylike("isin", element, test_elements)
-  result = _in1d(element, test_elements, invert=invert)
+  result = _in1d(element, test_elements, invert=invert,
+                 method=method, assume_unique=assume_unique)
   return result.reshape(np.shape(element))
```

```json
{
  "old_file": "R_candidates/Vi-1_jax-v0.4.31/jax._src.numpy.setops.isin.py",
  "new_file": "R_candidates/Vi_jax-v0.4.32/jax._src.numpy.setops.isin.py",
  "lines_added": 4,
  "lines_removed": 3
}
```
