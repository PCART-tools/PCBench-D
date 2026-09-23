# 一、突变情况分析

- **Total**: 4959
- **替代API**: `matplotlib.backend_bases.GraphicsContextBase.set_foreground`
- **10% 阈值**: 495.9

## Vi-1 (v1.2.1-v2.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 3312 | 0.3800 |
| tokenBased | 949 | 0.2800 |
| treeBased | 3290 | 0.3521 |

## Vi (v1.3.0-v2.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2244 | 0.4496 |
| tokenBased | 502 | 0.3600 |
| treeBased | 3152 | 0.4416 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 3312 | 2244 | +1068 | true |
| tokenBased | 949 | 502 | +447 | false |
| treeBased | 3290 | 3152 | +138 | false |

```json
{
  "total": 4959,
  "replacement_api": "matplotlib.backend_bases.GraphicsContextBase.set_foreground",
  "threshold_10pct": 495.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 3312,
      "score": 0.380022
    },
    "tokenBased": {
      "rank": 949,
      "score": 0.28
    },
    "treeBased": {
      "rank": 3290,
      "score": 0.352113
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2244,
      "score": 0.449584
    },
    "tokenBased": {
      "rank": 502,
      "score": 0.36
    },
    "treeBased": {
      "rank": 3152,
      "score": 0.441558
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 3312,
      "vi_rank": 2244,
      "delta": 1068,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 949,
      "vi_rank": 502,
      "delta": 447,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 3290,
      "vi_rank": 3152,
      "delta": 138,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.backend_bases.GraphicsContextBase.set_graylevel/Vi-1_v1.2.1.py`
- **new**: `matplotlib.backend_bases.GraphicsContextBase.set_graylevel/Vi_v1.3.0.py`
- **+2 / -1**

```diff
--- matplotlib.backend_bases.GraphicsContextBase.set_graylevel/Vi-1_v1.2.1.py
+++ matplotlib.backend_bases.GraphicsContextBase.set_graylevel/Vi_v1.3.0.py
@@ -1,3 +1,4 @@
     def set_graylevel(self, frac):
         
-        self._rgb = (frac, frac, frac)
+        self._orig_color = frac
+        self._rgb = (frac, frac, frac, self._alpha)
```

```json
{
  "old_file": "matplotlib.backend_bases.GraphicsContextBase.set_graylevel/Vi-1_v1.2.1.py",
  "new_file": "matplotlib.backend_bases.GraphicsContextBase.set_graylevel/Vi_v1.3.0.py",
  "lines_added": 2,
  "lines_removed": 1
}
```
