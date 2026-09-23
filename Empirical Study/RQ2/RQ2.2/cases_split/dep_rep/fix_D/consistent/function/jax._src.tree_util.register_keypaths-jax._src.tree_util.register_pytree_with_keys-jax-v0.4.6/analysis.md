# 一、突变情况分析

- **Total**: 3152
- **替代API**: `jax._src.tree_util.register_pytree_with_keys`
- **10% 阈值**: 315.2

## Vi-1 (jax-v0.4.5-jax-v0.4.6)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 549 | 0.4991 |
| tokenBased | 5 | 0.2613 |
| treeBased | 830 | 0.3871 |

## Vi (jax-v0.4.5-jax-v0.4.7)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1645 | 0.3476 |
| tokenBased | 13 | 0.2308 |
| treeBased | 1505 | 0.3025 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 549 | 1645 | -1096 | true |
| tokenBased | 5 | 13 | -8 | false |
| treeBased | 830 | 1505 | -675 | true |

```json
{
  "total": 3152,
  "replacement_api": "jax._src.tree_util.register_pytree_with_keys",
  "threshold_10pct": 315.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 549,
      "score": 0.49911
    },
    "tokenBased": {
      "rank": 5,
      "score": 0.261261
    },
    "treeBased": {
      "rank": 830,
      "score": 0.387097
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1645,
      "score": 0.347578
    },
    "tokenBased": {
      "rank": 13,
      "score": 0.230769
    },
    "treeBased": {
      "rank": 1505,
      "score": 0.302521
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 549,
      "vi_rank": 1645,
      "delta": -1096,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 5,
      "vi_rank": 13,
      "delta": -8,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 830,
      "vi_rank": 1505,
      "delta": -675,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_jax-v0.4.6/jax._src.tree_util.register_pytree_with_keys.py`
- **new**: `R_candidates/Vi_jax-v0.4.7/jax._src.tree_util.register_pytree_with_keys.py`
- **+14 / -5**

```diff
--- R_candidates/Vi-1_jax-v0.4.6/jax._src.tree_util.register_pytree_with_keys.py
+++ R_candidates/Vi_jax-v0.4.7/jax._src.tree_util.register_pytree_with_keys.py
@@ -1,11 +1,20 @@
 def register_pytree_with_keys(
     nodetype: Type[T],
-    flatten_with_keys: Callable[[T], Tuple[Iterable[Tuple[KeyPath, _Children]], _AuxData]],
-    unflatten_func: Callable[[_AuxData, _Children], T]):
+    flatten_with_keys: Callable[
+        [T], Tuple[Iterable[Tuple[KeyEntry, Any]], _AuxData]
+    ],
+    unflatten_func: Callable[[_AuxData, Iterable[Any]], T],
+    flatten_func: Optional[
+        Callable[[T], Tuple[Iterable[Any], _AuxData]]
+    ] = None,
+):
   
-  def flatten_func(tree):
-    key_children, treedef = flatten_with_keys(tree)
-    return [c for _, c in key_children], treedef
+  if not flatten_func:
+    def flatten_func_impl(tree):
+      key_children, treedef = flatten_with_keys(tree)
+      return [c for _, c in key_children], treedef
+    flatten_func = flatten_func_impl
+
   register_pytree_node(nodetype, flatten_func, unflatten_func)
   _registry_with_keypaths[nodetype] = _RegistryWithKeypathsEntry(
       flatten_with_keys, unflatten_func
```

```json
{
  "old_file": "R_candidates/Vi-1_jax-v0.4.6/jax._src.tree_util.register_pytree_with_keys.py",
  "new_file": "R_candidates/Vi_jax-v0.4.7/jax._src.tree_util.register_pytree_with_keys.py",
  "lines_added": 14,
  "lines_removed": 5
}
```
