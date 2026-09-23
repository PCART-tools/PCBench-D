# 一、突变情况分析

- **Total**: 4959
- **替代API**: `matplotlib.backend_bases.GraphicsContextBase.set_foreground`
- **10% 阈值**: 495.9

## Vi-1 (v1.4.3-v2.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2244 | 0.4496 |
| tokenBased | 502 | 0.3600 |
| treeBased | 3152 | 0.4416 |

## Vi (v1.5.0-v2.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 3377 | 0.3705 |
| tokenBased | 178 | 0.4231 |
| treeBased | 3135 | 0.4390 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2244 | 3377 | -1133 | true |
| tokenBased | 502 | 178 | +324 | false |
| treeBased | 3152 | 3135 | +17 | false |

```json
{
  "total": 4959,
  "replacement_api": "matplotlib.backend_bases.GraphicsContextBase.set_foreground",
  "threshold_10pct": 495.9,
  "vi_minus_1": {
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
  "vi": {
    "mapBased": {
      "rank": 3377,
      "score": 0.370509
    },
    "tokenBased": {
      "rank": 178,
      "score": 0.423077
    },
    "treeBased": {
      "rank": 3135,
      "score": 0.439024
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2244,
      "vi_rank": 3377,
      "delta": -1133,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 502,
      "vi_rank": 178,
      "delta": 324,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 3152,
      "vi_rank": 3135,
      "delta": 17,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.backend_bases.GraphicsContextBase.set_graylevel/Vi-1_v1.4.3.py`
- **new**: `matplotlib.backend_bases.GraphicsContextBase.set_graylevel/Vi_v1.5.0.py`
- **+5 / -1**

```diff
--- matplotlib.backend_bases.GraphicsContextBase.set_graylevel/Vi-1_v1.4.3.py
+++ matplotlib.backend_bases.GraphicsContextBase.set_graylevel/Vi_v1.5.0.py
@@ -1,4 +1,8 @@
     def set_graylevel(self, frac):
         
-        self._orig_color = frac
+
+        msg = ("set_graylevel is deprecated for removal in 1.6; "
+                "you can achieve the same result by using "
+                "set_foreground((frac, frac, frac))")
+        warnings.warn(msg, mplDeprecation)
         self._rgb = (frac, frac, frac, self._alpha)
```

```json
{
  "old_file": "matplotlib.backend_bases.GraphicsContextBase.set_graylevel/Vi-1_v1.4.3.py",
  "new_file": "matplotlib.backend_bases.GraphicsContextBase.set_graylevel/Vi_v1.5.0.py",
  "lines_added": 5,
  "lines_removed": 1
}
```
