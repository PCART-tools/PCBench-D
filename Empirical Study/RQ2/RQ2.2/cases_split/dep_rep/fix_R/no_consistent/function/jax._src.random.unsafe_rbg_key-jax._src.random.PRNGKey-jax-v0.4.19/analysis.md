# 一、突变情况分析

- **Total**: 3838
- **替代API**: `jax._src.random.PRNGKey`
- **10% 阈值**: 383.8

## Vi-1 (jax-v0.4.19-jax-v0.4.24)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 775 | 0.5333 |
| tokenBased | 432 | 0.2973 |
| treeBased | 1050 | 0.4364 |

## Vi (jax-v0.4.20-jax-v0.4.24)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 775 | 0.5333 |
| tokenBased | 14 | 0.4595 |
| treeBased | 286 | 0.4912 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 775 | 775 | +0 | false |
| tokenBased | 432 | 14 | +418 | true |
| treeBased | 1050 | 286 | +764 | true |

```json
{
  "total": 3838,
  "replacement_api": "jax._src.random.PRNGKey",
  "threshold_10pct": 383.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 775,
      "score": 0.533333
    },
    "tokenBased": {
      "rank": 432,
      "score": 0.297297
    },
    "treeBased": {
      "rank": 1050,
      "score": 0.436364
    }
  },
  "vi": {
    "mapBased": {
      "rank": 775,
      "score": 0.533333
    },
    "tokenBased": {
      "rank": 14,
      "score": 0.459459
    },
    "treeBased": {
      "rank": 286,
      "score": 0.491228
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 775,
      "vi_rank": 775,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 432,
      "vi_rank": 14,
      "delta": 418,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1050,
      "vi_rank": 286,
      "delta": 764,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `jax._src.random.unsafe_rbg_key/Vi-1_jax-v0.4.19.py`
- **new**: `jax._src.random.unsafe_rbg_key/Vi_jax-v0.4.20.py`
- **+1 / -1**

```diff
--- jax._src.random.unsafe_rbg_key/Vi-1_jax-v0.4.19.py
+++ jax._src.random.unsafe_rbg_key/Vi_jax-v0.4.20.py
@@ -1,4 +1,4 @@
-def unsafe_rbg_key(seed: int) -> KeyArray:
+def unsafe_rbg_key(seed: int | ArrayLike) -> KeyArray:
   
   impl = prng.unsafe_rbg_prng_impl
   _check_default_impl_with_no_custom_prng(impl, 'unsafe_rbg')
```

```json
{
  "old_file": "jax._src.random.unsafe_rbg_key/Vi-1_jax-v0.4.19.py",
  "new_file": "jax._src.random.unsafe_rbg_key/Vi_jax-v0.4.20.py",
  "lines_added": 1,
  "lines_removed": 1
}
```
