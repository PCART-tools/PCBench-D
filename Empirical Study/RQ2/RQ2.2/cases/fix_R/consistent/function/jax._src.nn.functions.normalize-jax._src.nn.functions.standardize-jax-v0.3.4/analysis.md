# 一、突变情况分析

- **Total**: 43
- **替代API**: `jax._src.nn.functions.standardize`
- **10% 阈值**: 4.3

## Vi-1 (jax-v0.3.4-jax-v0.4.21)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9124 |
| tokenBased | 1 | 0.6826 |
| treeBased | 1 | 0.8707 |

## Vi (jax-v0.3.5-jax-v0.4.21)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 16 | 0.5930 |
| tokenBased | 3 | 0.4643 |
| treeBased | 8 | 0.5615 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 16 | -15 | true |
| tokenBased | 1 | 3 | -2 | false |
| treeBased | 1 | 8 | -7 | true |

```json
{
  "total": 43,
  "replacement_api": "jax._src.nn.functions.standardize",
  "threshold_10pct": 4.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.912409
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.682635
    },
    "treeBased": {
      "rank": 1,
      "score": 0.87069
    }
  },
  "vi": {
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
      "score": 0.561497
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 16,
      "delta": -15,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 3,
      "delta": -2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 8,
      "delta": -7,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `jax._src.nn.functions.normalize/Vi-1_jax-v0.3.4.py`
- **new**: `jax._src.nn.functions.normalize/Vi_jax-v0.3.5.py`
- **+2 / -11**

```diff
--- jax._src.nn.functions.normalize/Vi-1_jax-v0.3.4.py
+++ jax._src.nn.functions.normalize/Vi_jax-v0.3.5.py
@@ -1,4 +1,3 @@
-@partial(jax.jit, static_argnames=("axis",))
 def normalize(x: Array,
               axis: Optional[Union[int, Tuple[int, ...]]] = -1,
               mean: Optional[Array] = None,
@@ -6,13 +5,5 @@
               epsilon: Array = 1e-5,
               where: Optional[Array] = None) -> Array:
   
-  if mean is None:
-    mean = jnp.mean(x, axis, keepdims=True, where=where)
-  if variance is None:
-
-
-
-
-    variance = jnp.mean(
-        jnp.square(x), axis, keepdims=True, where=where) - jnp.square(mean)
-  return (x - mean) * lax.rsqrt(variance + epsilon)
+  warnings.warn("jax.nn.normalize will be deprecated. Use jax.nn.standardize instead.", DeprecationWarning)
+  return standardize(x, axis, mean, variance, epsilon, where)
```

```json
{
  "old_file": "jax._src.nn.functions.normalize/Vi-1_jax-v0.3.4.py",
  "new_file": "jax._src.nn.functions.normalize/Vi_jax-v0.3.5.py",
  "lines_added": 2,
  "lines_removed": 11
}
```
