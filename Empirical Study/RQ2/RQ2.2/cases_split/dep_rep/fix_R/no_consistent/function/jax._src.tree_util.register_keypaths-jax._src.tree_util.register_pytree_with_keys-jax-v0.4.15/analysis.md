# 一、突变情况分析

- **Total**: 3838
- **替代API**: `jax._src.tree_util.register_pytree_with_keys`
- **10% 阈值**: 383.8

## Vi-1 (jax-v0.4.15-jax-v0.4.24)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 92 | 0.5899 |
| tokenBased | 4 | 0.3071 |
| treeBased | 767 | 0.4091 |

## Vi (jax-v0.4.16-jax-v0.4.24)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 731 | 0.5201 |
| tokenBased | 4 | 0.2941 |
| treeBased | 1213 | 0.3659 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 92 | 731 | -639 | true |
| tokenBased | 4 | 4 | +0 | false |
| treeBased | 767 | 1213 | -446 | true |

```json
{
  "total": 3838,
  "replacement_api": "jax._src.tree_util.register_pytree_with_keys",
  "threshold_10pct": 383.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 92,
      "score": 0.589912
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.307143
    },
    "treeBased": {
      "rank": 767,
      "score": 0.409091
    }
  },
  "vi": {
    "mapBased": {
      "rank": 731,
      "score": 0.520119
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.294118
    },
    "treeBased": {
      "rank": 1213,
      "score": 0.365854
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 92,
      "vi_rank": 731,
      "delta": -639,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 4,
      "vi_rank": 4,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 767,
      "vi_rank": 1213,
      "delta": -446,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `jax._src.tree_util.register_keypaths/Vi-1_jax-v0.4.15.py`
- **new**: `jax._src.tree_util.register_keypaths/Vi_jax-v0.4.16.py`
- **+0 / -9**

```diff
--- jax._src.tree_util.register_keypaths/Vi-1_jax-v0.4.15.py
+++ jax._src.tree_util.register_keypaths/Vi_jax-v0.4.16.py
@@ -2,13 +2,4 @@
     ty: type[T], handler: Callable[[T], tuple[KeyEntry, ...]]
 ) -> None:
   
-  warnings.warn(
-      (
-          "jax.tree_util.register_keypaths is deprecated, and will be removed"
-          " in a future release. Please use `register_pytree_with_keys()`"
-          " instead."
-      ),
-      category=FutureWarning,
-      stacklevel=2,
-  )
   _register_keypaths(ty, handler)
```

```json
{
  "old_file": "jax._src.tree_util.register_keypaths/Vi-1_jax-v0.4.15.py",
  "new_file": "jax._src.tree_util.register_keypaths/Vi_jax-v0.4.16.py",
  "lines_added": 0,
  "lines_removed": 9
}
```
