# 一、突变情况分析

- **Total**: 4803
- **替代API**: `matplotlib.backend_bases.FigureCanvasBase.set_cursor`
- **10% 阈值**: 480.3

## Vi-1 (v3.4.3-v3.7.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 1.0000 |
| treeBased | 1 | 1.0000 |

## Vi (v3.5.0-v3.7.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 205 | 0.7978 |
| tokenBased | 3 | 0.6471 |
| treeBased | 1222 | 0.5385 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 205 | -204 | false |
| tokenBased | 1 | 3 | -2 | false |
| treeBased | 1 | 1222 | -1221 | true |

```json
{
  "total": 4803,
  "replacement_api": "matplotlib.backend_bases.FigureCanvasBase.set_cursor",
  "threshold_10pct": 480.3,
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
      "rank": 205,
      "score": 0.797753
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.647059
    },
    "treeBased": {
      "rank": 1222,
      "score": 0.538462
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 205,
      "delta": -204,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 3,
      "delta": -2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 1222,
      "delta": -1221,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.backend_bases.NavigationToolbar2.set_cursor/Vi-1_v3.4.3.py`
- **new**: `matplotlib.backend_bases.NavigationToolbar2.set_cursor/Vi_v3.5.0.py`
- **+2 / -0**

```diff
--- matplotlib.backend_bases.NavigationToolbar2.set_cursor/Vi-1_v3.4.3.py
+++ matplotlib.backend_bases.NavigationToolbar2.set_cursor/Vi_v3.5.0.py
@@ -1,2 +1,4 @@
+    @_api.deprecated("3.5", alternative="canvas.set_cursor")
     def set_cursor(self, cursor):
         
+        self.canvas.set_cursor(cursor)
```

```json
{
  "old_file": "matplotlib.backend_bases.NavigationToolbar2.set_cursor/Vi-1_v3.4.3.py",
  "new_file": "matplotlib.backend_bases.NavigationToolbar2.set_cursor/Vi_v3.5.0.py",
  "lines_added": 2,
  "lines_removed": 0
}
```
