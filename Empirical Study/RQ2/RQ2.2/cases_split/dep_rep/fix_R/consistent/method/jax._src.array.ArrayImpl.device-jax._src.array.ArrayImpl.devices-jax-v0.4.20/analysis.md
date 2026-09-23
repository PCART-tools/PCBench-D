# 一、突变情况分析

- **Total**: 1442
- **替代API**: `jax._src.array.ArrayImpl.devices`
- **10% 阈值**: 144.2

## Vi-1 (jax-v0.4.20-jax-v0.4.27)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 76 | 0.5477 |
| tokenBased | 241 | 0.3077 |
| treeBased | 9 | 0.5490 |

## Vi (jax-v0.4.21-jax-v0.4.27)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 226 | 0.4564 |
| tokenBased | 389 | 0.2609 |
| treeBased | 41 | 0.4746 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 76 | 226 | -150 | true |
| tokenBased | 241 | 389 | -148 | true |
| treeBased | 9 | 41 | -32 | false |

```json
{
  "total": 1442,
  "replacement_api": "jax._src.array.ArrayImpl.devices",
  "threshold_10pct": 144.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 76,
      "score": 0.547697
    },
    "tokenBased": {
      "rank": 241,
      "score": 0.307692
    },
    "treeBased": {
      "rank": 9,
      "score": 0.54902
    }
  },
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 76,
      "vi_rank": 226,
      "delta": -150,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 241,
      "vi_rank": 389,
      "delta": -148,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 9,
      "vi_rank": 41,
      "delta": -32,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `jax._src.array.ArrayImpl.device/Vi-1_jax-v0.4.20.py`
- **new**: `jax._src.array.ArrayImpl.device/Vi_jax-v0.4.21.py`
- **+2 / -0**

```diff
--- jax._src.array.ArrayImpl.device/Vi-1_jax-v0.4.20.py
+++ jax._src.array.ArrayImpl.device/Vi_jax-v0.4.21.py
@@ -1,4 +1,6 @@
   def device(self) -> Device:
+    warnings.warn("arr.device() is deprecated. Use arr.devices() instead.",
+                  DeprecationWarning, stacklevel=2)
     self._check_if_deleted()
     device_set = self.sharding.device_set
     if len(device_set) == 1:
```

```json
{
  "old_file": "jax._src.array.ArrayImpl.device/Vi-1_jax-v0.4.20.py",
  "new_file": "jax._src.array.ArrayImpl.device/Vi_jax-v0.4.21.py",
  "lines_added": 2,
  "lines_removed": 0
}
```
