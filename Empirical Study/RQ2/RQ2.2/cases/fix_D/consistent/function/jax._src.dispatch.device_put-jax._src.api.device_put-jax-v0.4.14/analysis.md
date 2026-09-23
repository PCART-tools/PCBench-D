# 一、突变情况分析

- **Total**: 3357
- **替代API**: `jax._src.api.device_put`
- **10% 阈值**: 335.7

## Vi-1 (jax-v0.4.6-jax-v0.4.14)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2301 | 0.3367 |
| tokenBased | 1278 | 0.2298 |
| treeBased | 2326 | 0.3258 |

## Vi (jax-v0.4.6-jax-v0.4.15)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2453 | 0.3367 |
| tokenBased | 1751 | 0.2067 |
| treeBased | 2591 | 0.3152 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2301 | 2453 | -152 | false |
| tokenBased | 1278 | 1751 | -473 | true |
| treeBased | 2326 | 2591 | -265 | false |

```json
{
  "total": 3357,
  "replacement_api": "jax._src.api.device_put",
  "threshold_10pct": 335.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2301,
      "score": 0.336652
    },
    "tokenBased": {
      "rank": 1278,
      "score": 0.229814
    },
    "treeBased": {
      "rank": 2326,
      "score": 0.325843
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2453,
      "score": 0.336652
    },
    "tokenBased": {
      "rank": 1751,
      "score": 0.206704
    },
    "treeBased": {
      "rank": 2591,
      "score": 0.315217
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2301,
      "vi_rank": 2453,
      "delta": -152,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1278,
      "vi_rank": 1751,
      "delta": -473,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2326,
      "vi_rank": 2591,
      "delta": -265,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_jax-v0.4.14/jax._src.api.device_put.py`
- **new**: `R_candidates/Vi_jax-v0.4.15/jax._src.api.device_put.py`
- **+8 / -6**

```diff
--- R_candidates/Vi-1_jax-v0.4.14/jax._src.api.device_put.py
+++ R_candidates/Vi_jax-v0.4.15/jax._src.api.device_put.py
@@ -1,11 +1,13 @@
 def device_put(
     x,
-    device: None | xc.Device | Sharding | Any = None,
-    *, src: None | xc.Device | Sharding | Any = None):
+    device: None | xc.Device | Sharding | Any | TransferToMemoryKind = None,
+    *, src: None | xc.Device | Sharding | Any | TransferToMemoryKind = None):
   
   with config_explicit_device_put_scope():
-    if ((device is None or isinstance(device, (xc.Device, Sharding))) and
-        (src is None or isinstance(src, (xc.Device, Sharding)))):
+    if ((device is None or
+         isinstance(device, (xc.Device, Sharding, TransferToMemoryKind))) and
+        (src is None or
+         isinstance(src, (xc.Device, Sharding, TransferToMemoryKind)))):
       return tree_map(
           lambda y: dispatch.device_put_p.bind(
               y, device=device, src=_infer_src_sharding(src, y)), x)
@@ -14,7 +16,7 @@
     device_flat = flatten_axes("device_put device", treedef, device)
     src_flat = flatten_axes("device_put source", treedef, src)
     out_flat = [
-        dispatch.device_put_p.bind(y, device=d, src=_infer_src_sharding(s, y))
-        for y, d, s in zip(x_flat, device_flat, src_flat)
+        dispatch.device_put_p.bind(xf, device=d, src=_infer_src_sharding(s, xf))
+        for xf, d, s in zip(x_flat, device_flat, src_flat)
     ]
     return tree_unflatten(treedef, out_flat)
```

```json
{
  "old_file": "R_candidates/Vi-1_jax-v0.4.14/jax._src.api.device_put.py",
  "new_file": "R_candidates/Vi_jax-v0.4.15/jax._src.api.device_put.py",
  "lines_added": 8,
  "lines_removed": 6
}
```
