# 一、突变情况分析

- **Total**: 272
- **替代API**: `matplotlib.axes._subplots.SubplotBase.get_subplotspec`
- **10% 阈值**: 27.2

## Vi-1 (v3.3.4-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 25 | 0.6502 |
| tokenBased | 66 | 0.2812 |
| treeBased | 84 | 0.4545 |

## Vi (v3.4.0-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 25 | 0.6502 |
| tokenBased | 69 | 0.2727 |
| treeBased | 138 | 0.3659 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 25 | 25 | +0 | false |
| tokenBased | 66 | 69 | -3 | false |
| treeBased | 84 | 138 | -54 | true |

```json
{
  "total": 272,
  "replacement_api": "matplotlib.axes._subplots.SubplotBase.get_subplotspec",
  "threshold_10pct": 27.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 25,
      "score": 0.650198
    },
    "tokenBased": {
      "rank": 66,
      "score": 0.28125
    },
    "treeBased": {
      "rank": 84,
      "score": 0.454545
    }
  },
  "vi": {
    "mapBased": {
      "rank": 25,
      "score": 0.650198
    },
    "tokenBased": {
      "rank": 69,
      "score": 0.272727
    },
    "treeBased": {
      "rank": 138,
      "score": 0.365854
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 25,
      "vi_rank": 25,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 66,
      "vi_rank": 69,
      "delta": -3,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 84,
      "vi_rank": 138,
      "delta": -54,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.axes._subplots.SubplotBase.get_geometry/Vi-1_v3.3.4.py`
- **new**: `matplotlib.axes._subplots.SubplotBase.get_geometry/Vi_v3.4.0.py`
- **+3 / -0**

```diff
--- matplotlib.axes._subplots.SubplotBase.get_geometry/Vi-1_v3.3.4.py
+++ matplotlib.axes._subplots.SubplotBase.get_geometry/Vi_v3.4.0.py
@@ -1,3 +1,6 @@
+    @_api.deprecated(
+        "3.4", alternative="get_subplotspec",
+        addendum="(get_subplotspec returns a SubplotSpec instance.)")
     def get_geometry(self):
         
         rows, cols, num1, num2 = self.get_subplotspec().get_geometry()
```

```json
{
  "old_file": "matplotlib.axes._subplots.SubplotBase.get_geometry/Vi-1_v3.3.4.py",
  "new_file": "matplotlib.axes._subplots.SubplotBase.get_geometry/Vi_v3.4.0.py",
  "lines_added": 3,
  "lines_removed": 0
}
```
