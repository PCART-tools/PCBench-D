# 一、突变情况分析

- **Total**: 4807
- **替代API**: `matplotlib.backend_bases.FigureManagerBase.resize`
- **10% 阈值**: 480.7

## Vi-1 (v3.5.3-v3.8.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 1.0000 |
| treeBased | 1 | 1.0000 |

## Vi (v3.6.0-v3.8.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 171 | 0.6718 |
| tokenBased | 1348 | 0.2647 |
| treeBased | 3028 | 0.3810 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 171 | -170 | false |
| tokenBased | 1 | 1348 | -1347 | true |
| treeBased | 1 | 3028 | -3027 | true |

```json
{
  "total": 4807,
  "replacement_api": "matplotlib.backend_bases.FigureManagerBase.resize",
  "threshold_10pct": 480.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 1.0
    },
    "treeBased": {
      "rank": 1,
      "score": 1.0
    }
  },
  "vi": {
    "mapBased": {
      "rank": 171,
      "score": 0.671756
    },
    "tokenBased": {
      "rank": 1348,
      "score": 0.264706
    },
    "treeBased": {
      "rank": 3028,
      "score": 0.380952
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 171,
      "delta": -170,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 1348,
      "delta": -1347,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 3028,
      "delta": -3027,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.backend_bases.FigureCanvasBase.resize/Vi-1_v3.5.3.py`
- **new**: `matplotlib.backend_bases.FigureCanvasBase.resize/Vi_v3.6.0.py`
- **+7 / -0**

```diff
--- matplotlib.backend_bases.FigureCanvasBase.resize/Vi-1_v3.5.3.py
+++ matplotlib.backend_bases.FigureCanvasBase.resize/Vi_v3.6.0.py
@@ -1,2 +1,9 @@
     def resize(self, w, h):
         
+
+
+        if hasattr(super(), "resize"):
+            return super().resize(w, h)
+        else:
+            _api.warn_deprecated("3.6", name="resize", obj_type="method",
+                                 alternative="FigureManagerBase.resize")
```

```json
{
  "old_file": "matplotlib.backend_bases.FigureCanvasBase.resize/Vi-1_v3.5.3.py",
  "new_file": "matplotlib.backend_bases.FigureCanvasBase.resize/Vi_v3.6.0.py",
  "lines_added": 7,
  "lines_removed": 0
}
```
