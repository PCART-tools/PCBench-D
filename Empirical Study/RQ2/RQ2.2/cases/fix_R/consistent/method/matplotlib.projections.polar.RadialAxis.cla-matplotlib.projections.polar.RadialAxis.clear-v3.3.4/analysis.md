# 一、突变情况分析

- **Total**: 152
- **替代API**: `matplotlib.projections.polar.RadialAxis.clear`
- **10% 阈值**: 15.2

## Vi-1 (v3.3.4-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9961 |
| tokenBased | 1 | 0.6667 |
| treeBased | 1 | 0.9500 |

## Vi (v3.4.0-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 11 | 0.6355 |
| tokenBased | 13 | 0.2917 |
| treeBased | 21 | 0.5833 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 11 | -10 | false |
| tokenBased | 1 | 13 | -12 | false |
| treeBased | 1 | 21 | -20 | true |

```json
{
  "total": 152,
  "replacement_api": "matplotlib.projections.polar.RadialAxis.clear",
  "threshold_10pct": 15.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.996128
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.666667
    },
    "treeBased": {
      "rank": 1,
      "score": 0.95
    }
  },
  "vi": {
    "mapBased": {
      "rank": 11,
      "score": 0.635534
    },
    "tokenBased": {
      "rank": 13,
      "score": 0.291667
    },
    "treeBased": {
      "rank": 21,
      "score": 0.583333
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 11,
      "delta": -10,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 13,
      "delta": -12,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 21,
      "delta": -20,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.projections.polar.RadialAxis.cla/Vi-1_v3.3.4.py`
- **new**: `matplotlib.projections.polar.RadialAxis.cla/Vi_v3.4.0.py`
- **+2 / -3**

```diff
--- matplotlib.projections.polar.RadialAxis.cla/Vi-1_v3.3.4.py
+++ matplotlib.projections.polar.RadialAxis.cla/Vi_v3.4.0.py
@@ -1,4 +1,3 @@
+    @_api.deprecated("3.4", alternative="RadialAxis.clear()")
     def cla(self):
-        super().cla()
-        self.set_ticks_position('none')
-        self._wrap_locator_formatter()
+        self.clear()
```

```json
{
  "old_file": "matplotlib.projections.polar.RadialAxis.cla/Vi-1_v3.3.4.py",
  "new_file": "matplotlib.projections.polar.RadialAxis.cla/Vi_v3.4.0.py",
  "lines_added": 2,
  "lines_removed": 3
}
```
