# 一、突变情况分析

- **Total**: 4834
- **替代API**: `matplotlib.backend_bases.FigureManagerBase.get_window_title`
- **10% 阈值**: 483.4

## Vi-1 (v3.3.4-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 444 | 0.7083 |
| tokenBased | 5 | 0.6087 |
| treeBased | 1088 | 0.5769 |

## Vi (v3.4.0-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 444 | 0.7083 |
| tokenBased | 5 | 0.5833 |
| treeBased | 1827 | 0.4688 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 444 | 444 | +0 | false |
| tokenBased | 5 | 5 | +0 | false |
| treeBased | 1088 | 1827 | -739 | true |

```json
{
  "total": 4834,
  "replacement_api": "matplotlib.backend_bases.FigureManagerBase.get_window_title",
  "threshold_10pct": 483.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 444,
      "score": 0.708333
    },
    "tokenBased": {
      "rank": 5,
      "score": 0.608696
    },
    "treeBased": {
      "rank": 1088,
      "score": 0.576923
    }
  },
  "vi": {
    "mapBased": {
      "rank": 444,
      "score": 0.708333
    },
    "tokenBased": {
      "rank": 5,
      "score": 0.583333
    },
    "treeBased": {
      "rank": 1827,
      "score": 0.46875
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 444,
      "vi_rank": 444,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 5,
      "vi_rank": 5,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1088,
      "vi_rank": 1827,
      "delta": -739,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.backend_bases.FigureCanvasBase.get_window_title/Vi-1_v3.3.4.py`
- **new**: `matplotlib.backend_bases.FigureCanvasBase.get_window_title/Vi_v3.4.0.py`
- **+2 / -0**

```diff
--- matplotlib.backend_bases.FigureCanvasBase.get_window_title/Vi-1_v3.3.4.py
+++ matplotlib.backend_bases.FigureCanvasBase.get_window_title/Vi_v3.4.0.py
@@ -1,3 +1,5 @@
+    @_api.deprecated(
+        "3.4", alternative="manager.get_window_title or GUI-specific methods")
     def get_window_title(self):
         
         if self.manager is not None:
```

```json
{
  "old_file": "matplotlib.backend_bases.FigureCanvasBase.get_window_title/Vi-1_v3.3.4.py",
  "new_file": "matplotlib.backend_bases.FigureCanvasBase.get_window_title/Vi_v3.4.0.py",
  "lines_added": 2,
  "lines_removed": 0
}
```
