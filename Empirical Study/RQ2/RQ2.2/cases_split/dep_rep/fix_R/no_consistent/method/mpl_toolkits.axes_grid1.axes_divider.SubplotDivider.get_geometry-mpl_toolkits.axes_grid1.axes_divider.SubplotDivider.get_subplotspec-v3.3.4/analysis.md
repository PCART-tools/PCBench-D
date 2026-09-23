# 一、突变情况分析

- **Total**: 154
- **替代API**: `mpl_toolkits.axes_grid1.axes_divider.SubplotDivider.get_subplotspec`
- **10% 阈值**: 15.4

## Vi-1 (v3.3.4-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 18 | 0.6502 |
| tokenBased | 67 | 0.2812 |
| treeBased | 70 | 0.4545 |

## Vi (v3.4.0-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 18 | 0.6502 |
| tokenBased | 70 | 0.2727 |
| treeBased | 109 | 0.3659 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 18 | 18 | +0 | false |
| tokenBased | 67 | 70 | -3 | false |
| treeBased | 70 | 109 | -39 | true |

```json
{
  "total": 154,
  "replacement_api": "mpl_toolkits.axes_grid1.axes_divider.SubplotDivider.get_subplotspec",
  "threshold_10pct": 15.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 18,
      "score": 0.650198
    },
    "tokenBased": {
      "rank": 67,
      "score": 0.28125
    },
    "treeBased": {
      "rank": 70,
      "score": 0.454545
    }
  },
  "vi": {
    "mapBased": {
      "rank": 18,
      "score": 0.650198
    },
    "tokenBased": {
      "rank": 70,
      "score": 0.272727
    },
    "treeBased": {
      "rank": 109,
      "score": 0.365854
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 18,
      "vi_rank": 18,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 67,
      "vi_rank": 70,
      "delta": -3,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 70,
      "vi_rank": 109,
      "delta": -39,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `mpl_toolkits.axes_grid1.axes_divider.SubplotDivider.get_geometry/Vi-1_v3.3.4.py`
- **new**: `mpl_toolkits.axes_grid1.axes_divider.SubplotDivider.get_geometry/Vi_v3.4.0.py`
- **+3 / -0**

```diff
--- mpl_toolkits.axes_grid1.axes_divider.SubplotDivider.get_geometry/Vi-1_v3.3.4.py
+++ mpl_toolkits.axes_grid1.axes_divider.SubplotDivider.get_geometry/Vi_v3.4.0.py
@@ -1,3 +1,6 @@
+    @_api.deprecated(
+        "3.4", alternative="get_subplotspec",
+        addendum="(get_subplotspec returns a SubplotSpec instance.)")
     def get_geometry(self):
         
         rows, cols, num1, num2 = self.get_subplotspec().get_geometry()
```

```json
{
  "old_file": "mpl_toolkits.axes_grid1.axes_divider.SubplotDivider.get_geometry/Vi-1_v3.3.4.py",
  "new_file": "mpl_toolkits.axes_grid1.axes_divider.SubplotDivider.get_geometry/Vi_v3.4.0.py",
  "lines_added": 3,
  "lines_removed": 0
}
```
