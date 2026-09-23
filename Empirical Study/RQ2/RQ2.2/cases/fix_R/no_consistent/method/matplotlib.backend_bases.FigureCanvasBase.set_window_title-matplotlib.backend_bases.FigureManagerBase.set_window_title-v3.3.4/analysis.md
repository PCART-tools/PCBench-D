# 一、突变情况分析

- **Total**: 4834
- **替代API**: `matplotlib.backend_bases.FigureManagerBase.set_window_title`
- **10% 阈值**: 483.4

## Vi-1 (v3.3.4-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 266 | 0.6893 |
| tokenBased | 6 | 0.6087 |
| treeBased | 1914 | 0.5185 |

## Vi (v3.4.0-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 266 | 0.6893 |
| tokenBased | 6 | 0.5833 |
| treeBased | 2856 | 0.4242 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 266 | 266 | +0 | false |
| tokenBased | 6 | 6 | +0 | false |
| treeBased | 1914 | 2856 | -942 | true |

```json
{
  "total": 4834,
  "replacement_api": "matplotlib.backend_bases.FigureManagerBase.set_window_title",
  "threshold_10pct": 483.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 266,
      "score": 0.68932
    },
    "tokenBased": {
      "rank": 6,
      "score": 0.608696
    },
    "treeBased": {
      "rank": 1914,
      "score": 0.518519
    }
  },
  "vi": {
    "mapBased": {
      "rank": 266,
      "score": 0.68932
    },
    "tokenBased": {
      "rank": 6,
      "score": 0.583333
    },
    "treeBased": {
      "rank": 2856,
      "score": 0.424242
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 266,
      "vi_rank": 266,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 6,
      "vi_rank": 6,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1914,
      "vi_rank": 2856,
      "delta": -942,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.backend_bases.FigureCanvasBase.set_window_title/Vi-1_v3.3.4.py`
- **new**: `matplotlib.backend_bases.FigureCanvasBase.set_window_title/Vi_v3.4.0.py`
- **+2 / -0**

```diff
--- matplotlib.backend_bases.FigureCanvasBase.set_window_title/Vi-1_v3.3.4.py
+++ matplotlib.backend_bases.FigureCanvasBase.set_window_title/Vi_v3.4.0.py
@@ -1,3 +1,5 @@
+    @_api.deprecated(
+        "3.4", alternative="manager.set_window_title or GUI-specific methods")
     def set_window_title(self, title):
         
         if self.manager is not None:
```

```json
{
  "old_file": "matplotlib.backend_bases.FigureCanvasBase.set_window_title/Vi-1_v3.3.4.py",
  "new_file": "matplotlib.backend_bases.FigureCanvasBase.set_window_title/Vi_v3.4.0.py",
  "lines_added": 2,
  "lines_removed": 0
}
```
