# 一、突变情况分析

- **Total**: 3838
- **替代API**: `jax._src.tree_util.register_pytree_with_keys`
- **10% 阈值**: 383.8

## Vi-1 (jax-v0.4.5-jax-v0.4.24)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1947 | 0.3476 |
| tokenBased | 9 | 0.2308 |
| treeBased | 1834 | 0.2941 |

## Vi (jax-v0.4.6-jax-v0.4.24)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 92 | 0.5899 |
| tokenBased | 4 | 0.3071 |
| treeBased | 1040 | 0.3939 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1947 | 92 | +1855 | true |
| tokenBased | 9 | 4 | +5 | false |
| treeBased | 1834 | 1040 | +794 | true |

```json
{
  "total": 3838,
  "replacement_api": "jax._src.tree_util.register_pytree_with_keys",
  "threshold_10pct": 383.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1947,
      "score": 0.347578
    },
    "tokenBased": {
      "rank": 9,
      "score": 0.230769
    },
    "treeBased": {
      "rank": 1834,
      "score": 0.294118
    }
  },
  "vi": {
    "mapBased": {
      "rank": 92,
      "score": 0.589912
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.307143
    },
    "treeBased": {
      "rank": 1040,
      "score": 0.393939
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1947,
      "vi_rank": 92,
      "delta": 1855,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 9,
      "vi_rank": 4,
      "delta": 5,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1834,
      "vi_rank": 1040,
      "delta": 794,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `jax._src.tree_util.register_keypaths/Vi-1_jax-v0.4.5.py`
- **new**: `jax._src.tree_util.register_keypaths/Vi_jax-v0.4.6.py`
- **+14 / -3**

```diff
--- jax._src.tree_util.register_keypaths/Vi-1_jax-v0.4.5.py
+++ jax._src.tree_util.register_keypaths/Vi_jax-v0.4.6.py
@@ -1,3 +1,14 @@
-def register_keypaths(ty: Type, handler: Callable[[Any], Sequence[KeyPathEntry]]
-                      ) -> None:
-  _keypath_registry[ty] = handler
+def register_keypaths(
+    ty: Type[T], handler: Callable[[T], Tuple[KeyEntry, ...]]
+) -> None:
+  
+  warnings.warn(
+      (
+          "jax.tree_util.register_keypaths is deprecated, and will be removed"
+          " in a future release. Please use `register_pytree_with_keys()`"
+          " instead."
+      ),
+      category=FutureWarning,
+      stacklevel=2,
+  )
+  _register_keypaths(ty, handler)
```

```json
{
  "old_file": "jax._src.tree_util.register_keypaths/Vi-1_jax-v0.4.5.py",
  "new_file": "jax._src.tree_util.register_keypaths/Vi_jax-v0.4.6.py",
  "lines_added": 14,
  "lines_removed": 3
}
```
