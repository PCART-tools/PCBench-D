# 一、突变情况分析

- **Total**: 43
- **替代API**: `jax._src.nn.functions.standardize`
- **10% 阈值**: 4.3

## Vi-1 (jax-v0.4.16-jax-v0.4.21)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 16 | 0.5930 |
| tokenBased | 3 | 0.4643 |
| treeBased | 8 | 0.5668 |

## Vi (jax-v0.4.17-jax-v0.4.21)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 16 | 0.5930 |
| tokenBased | 2 | 0.5833 |
| treeBased | 2 | 0.5936 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 16 | 16 | +0 | false |
| tokenBased | 3 | 2 | +1 | false |
| treeBased | 8 | 2 | +6 | true |

```json
{
  "total": 43,
  "replacement_api": "jax._src.nn.functions.standardize",
  "threshold_10pct": 4.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 16,
      "score": 0.593019
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.464286
    },
    "treeBased": {
      "rank": 8,
      "score": 0.566845
    }
  },
  "vi": {
    "mapBased": {
      "rank": 16,
      "score": 0.593019
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.583333
    },
    "treeBased": {
      "rank": 2,
      "score": 0.593583
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 16,
      "vi_rank": 16,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 3,
      "vi_rank": 2,
      "delta": 1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 8,
      "vi_rank": 2,
      "delta": 6,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `jax._src.nn.functions.normalize/Vi-1_jax-v0.4.16.py`
- **new**: `jax._src.nn.functions.normalize/Vi_jax-v0.4.17.py`
- **+6 / -6**

```diff
--- jax._src.nn.functions.normalize/Vi-1_jax-v0.4.16.py
+++ jax._src.nn.functions.normalize/Vi_jax-v0.4.17.py
@@ -1,9 +1,9 @@
-def normalize(x: Array,
-              axis: Optional[Union[int, tuple[int, ...]]] = -1,
-              mean: Optional[Array] = None,
-              variance: Optional[Array] = None,
-              epsilon: Array = 1e-5,
-              where: Optional[Array] = None) -> Array:
+def normalize(x: ArrayLike,
+            axis: Optional[Union[int, tuple[int, ...]]] = -1,
+            mean: Optional[ArrayLike] = None,
+            variance: Optional[ArrayLike] = None,
+            epsilon: ArrayLike = 1e-5,
+            where: Optional[ArrayLike] = None) -> Array:
   
   warnings.warn("jax.nn.normalize will be deprecated. Use jax.nn.standardize instead.", DeprecationWarning)
   return standardize(x, axis, mean, variance, epsilon, where)
```

```json
{
  "old_file": "jax._src.nn.functions.normalize/Vi-1_jax-v0.4.16.py",
  "new_file": "jax._src.nn.functions.normalize/Vi_jax-v0.4.17.py",
  "lines_added": 6,
  "lines_removed": 6
}
```
