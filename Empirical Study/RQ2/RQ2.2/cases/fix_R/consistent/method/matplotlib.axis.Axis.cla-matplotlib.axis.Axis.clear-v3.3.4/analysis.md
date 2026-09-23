# 一、突变情况分析

- **Total**: 4834
- **替代API**: `matplotlib.axis.Axis.clear`
- **10% 阈值**: 483.4

## Vi-1 (v3.3.4-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9985 |
| tokenBased | 1 | 0.8846 |
| treeBased | 1 | 0.9702 |

## Vi (v3.4.0-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 3324 | 0.2784 |
| tokenBased | 3888 | 0.0741 |
| treeBased | 3984 | 0.2157 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 3324 | -3323 | true |
| tokenBased | 1 | 3888 | -3887 | true |
| treeBased | 1 | 3984 | -3983 | true |

```json
{
  "total": 4834,
  "replacement_api": "matplotlib.axis.Axis.clear",
  "threshold_10pct": 483.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.998522
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.884615
    },
    "treeBased": {
      "rank": 1,
      "score": 0.970238
    }
  },
  "vi": {
    "mapBased": {
      "rank": 3324,
      "score": 0.278351
    },
    "tokenBased": {
      "rank": 3888,
      "score": 0.074074
    },
    "treeBased": {
      "rank": 3984,
      "score": 0.215686
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 3324,
      "delta": -3323,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 3888,
      "delta": -3887,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 3984,
      "delta": -3983,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.axis.Axis.cla/Vi-1_v3.3.4.py`
- **new**: `matplotlib.axis.Axis.cla/Vi_v3.4.0.py`
- **+2 / -22**

```diff
--- matplotlib.axis.Axis.cla/Vi-1_v3.3.4.py
+++ matplotlib.axis.Axis.cla/Vi_v3.4.0.py
@@ -1,24 +1,4 @@
+    @_api.deprecated("3.4", alternative="Axis.clear()")
     def cla(self):
         
-
-        self.label.set_text('')
-
-        self._set_scale('linear')
-
-
-        self.callbacks = cbook.CallbackRegistry()
-
-
-        self._major_tick_kw['gridOn'] = (
-                mpl.rcParams['axes.grid'] and
-                mpl.rcParams['axes.grid.which'] in ('both', 'major'))
-        self._minor_tick_kw['gridOn'] = (
-                mpl.rcParams['axes.grid'] and
-                mpl.rcParams['axes.grid.which'] in ('both', 'minor'))
-
-        self.reset_ticks()
-
-        self.converter = None
-        self.units = None
-        self.set_units(None)
-        self.stale = True
+        return self.clear()
```

```json
{
  "old_file": "matplotlib.axis.Axis.cla/Vi-1_v3.3.4.py",
  "new_file": "matplotlib.axis.Axis.cla/Vi_v3.4.0.py",
  "lines_added": 2,
  "lines_removed": 22
}
```
