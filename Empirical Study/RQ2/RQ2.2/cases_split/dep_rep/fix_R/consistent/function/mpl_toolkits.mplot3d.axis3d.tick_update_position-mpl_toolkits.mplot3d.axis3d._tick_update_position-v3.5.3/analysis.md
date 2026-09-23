# 一、突变情况分析

- **Total**: 171
- **替代API**: `mpl_toolkits.mplot3d.axis3d._tick_update_position`
- **10% 阈值**: 17.1

## Vi-1 (v3.5.3-v3.8.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.9706 |
| treeBased | 1 | 0.9750 |

## Vi (v3.6.0-v3.8.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 13 | 0.5393 |
| tokenBased | 4 | 0.3143 |
| treeBased | 43 | 0.3614 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 13 | -12 | false |
| tokenBased | 1 | 4 | -3 | false |
| treeBased | 1 | 43 | -42 | true |

```json
{
  "total": 171,
  "replacement_api": "mpl_toolkits.mplot3d.axis3d._tick_update_position",
  "threshold_10pct": 17.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.970588
    },
    "treeBased": {
      "rank": 1,
      "score": 0.975
    }
  },
  "vi": {
    "mapBased": {
      "rank": 13,
      "score": 0.539334
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.314286
    },
    "treeBased": {
      "rank": 43,
      "score": 0.361446
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 13,
      "delta": -12,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 4,
      "delta": -3,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 43,
      "delta": -42,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `mpl_toolkits.mplot3d.axis3d.tick_update_position/Vi-1_v3.5.3.py`
- **new**: `mpl_toolkits.mplot3d.axis3d.tick_update_position/Vi_v3.6.0.py`
- **+2 / -9**

```diff
--- mpl_toolkits.mplot3d.axis3d.tick_update_position/Vi-1_v3.5.3.py
+++ mpl_toolkits.mplot3d.axis3d.tick_update_position/Vi_v3.6.0.py
@@ -1,11 +1,4 @@
+@_api.deprecated("3.6", alternative="a vendored copy of _tick_update_position")
 def tick_update_position(tick, tickxs, tickys, labelpos):
     
-
-    tick.label1.set_position(labelpos)
-    tick.label2.set_position(labelpos)
-    tick.tick1line.set_visible(True)
-    tick.tick2line.set_visible(False)
-    tick.tick1line.set_linestyle('-')
-    tick.tick1line.set_marker('')
-    tick.tick1line.set_data(tickxs, tickys)
-    tick.gridline.set_data(0, 0)
+    _tick_update_position(tick, tickxs, tickys, labelpos)
```

```json
{
  "old_file": "mpl_toolkits.mplot3d.axis3d.tick_update_position/Vi-1_v3.5.3.py",
  "new_file": "mpl_toolkits.mplot3d.axis3d.tick_update_position/Vi_v3.6.0.py",
  "lines_added": 2,
  "lines_removed": 9
}
```
