# 一、突变情况分析

- **Total**: 4909
- **替代API**: `matplotlib.backend_bases.GraphicsContextBase.set_dashes`
- **10% 阈值**: 490.9

## Vi-1 (v1.5.3-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 36 | 0.6294 |
| tokenBased | 67 | 0.4603 |
| treeBased | 25 | 0.5761 |

## Vi (v2.0.0-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2458 | 0.4458 |
| tokenBased | 965 | 0.2500 |
| treeBased | 2765 | 0.4000 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 36 | 2458 | -2422 | true |
| tokenBased | 67 | 965 | -898 | true |
| treeBased | 25 | 2765 | -2740 | true |

```json
{
  "total": 4909,
  "replacement_api": "matplotlib.backend_bases.GraphicsContextBase.set_dashes",
  "threshold_10pct": 490.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 36,
      "score": 0.629398
    },
    "tokenBased": {
      "rank": 67,
      "score": 0.460317
    },
    "treeBased": {
      "rank": 25,
      "score": 0.576087
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2458,
      "score": 0.445809
    },
    "tokenBased": {
      "rank": 965,
      "score": 0.25
    },
    "treeBased": {
      "rank": 2765,
      "score": 0.4
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 36,
      "vi_rank": 2458,
      "delta": -2422,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 67,
      "vi_rank": 965,
      "delta": -898,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 25,
      "vi_rank": 2765,
      "delta": -2740,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.backend_bases.GraphicsContextBase.set_linestyle/Vi-1_v1.5.3.py`
- **new**: `matplotlib.backend_bases.GraphicsContextBase.set_linestyle/Vi_v2.0.0.py`
- **+0 / -9**

```diff
--- matplotlib.backend_bases.GraphicsContextBase.set_linestyle/Vi-1_v1.5.3.py
+++ matplotlib.backend_bases.GraphicsContextBase.set_linestyle/Vi_v2.0.0.py
@@ -1,12 +1,3 @@
     def set_linestyle(self, style):
         
-
-        if style in self.dashd:
-            offset, dashes = self.dashd[style]
-        elif isinstance(style, tuple):
-            offset, dashes = style
-        else:
-            raise ValueError('Unrecognized linestyle: %s' % str(style))
-
         self._linestyle = style
-        self.set_dashes(offset, dashes)
```

```json
{
  "old_file": "matplotlib.backend_bases.GraphicsContextBase.set_linestyle/Vi-1_v1.5.3.py",
  "new_file": "matplotlib.backend_bases.GraphicsContextBase.set_linestyle/Vi_v2.0.0.py",
  "lines_added": 0,
  "lines_removed": 9
}
```
