# 一、突变情况分析

- **Total**: 1442
- **替代API**: `jax._src.array.ArrayImpl.devices`
- **10% 阈值**: 144.2

## Vi-1 (jax-v0.4.24-jax-v0.4.27)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 226 | 0.4564 |
| tokenBased | 389 | 0.2609 |
| treeBased | 41 | 0.4746 |

## Vi (jax-v0.4.25-jax-v0.4.27)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 357 | 0.3513 |
| tokenBased | 509 | 0.2069 |
| treeBased | 280 | 0.3944 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 226 | 357 | -131 | false |
| tokenBased | 389 | 509 | -120 | false |
| treeBased | 41 | 280 | -239 | true |

```json
{
  "total": 1442,
  "replacement_api": "jax._src.array.ArrayImpl.devices",
  "threshold_10pct": 144.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 226,
      "score": 0.456404
    },
    "tokenBased": {
      "rank": 389,
      "score": 0.26087
    },
    "treeBased": {
      "rank": 41,
      "score": 0.474576
    }
  },
  "vi": {
    "mapBased": {
      "rank": 357,
      "score": 0.351305
    },
    "tokenBased": {
      "rank": 509,
      "score": 0.206897
    },
    "treeBased": {
      "rank": 280,
      "score": 0.394366
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 226,
      "vi_rank": 357,
      "delta": -131,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 389,
      "vi_rank": 509,
      "delta": -120,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 41,
      "vi_rank": 280,
      "delta": -239,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `jax._src.array.ArrayImpl.device/Vi-1_jax-v0.4.24.py`
- **new**: `jax._src.array.ArrayImpl.device/Vi_jax-v0.4.25.py`
- **+5 / -2**

```diff
--- jax._src.array.ArrayImpl.device/Vi-1_jax-v0.4.24.py
+++ jax._src.array.ArrayImpl.device/Vi_jax-v0.4.25.py
@@ -1,6 +1,9 @@
   def device(self) -> Device:
-    warnings.warn("arr.device() is deprecated. Use arr.devices() instead.",
-                  DeprecationWarning, stacklevel=2)
+    if deprecations.is_accelerated(__name__, "device-method"):
+      raise NotImplementedError("arr.device() is deprecated. Use arr.devices() instead.")
+    else:
+      warnings.warn("arr.device() is deprecated. Use arr.devices() instead.",
+                    DeprecationWarning, stacklevel=2)
     self._check_if_deleted()
     device_set = self.sharding.device_set
     if len(device_set) == 1:
```

```json
{
  "old_file": "jax._src.array.ArrayImpl.device/Vi-1_jax-v0.4.24.py",
  "new_file": "jax._src.array.ArrayImpl.device/Vi_jax-v0.4.25.py",
  "lines_added": 5,
  "lines_removed": 2
}
```
