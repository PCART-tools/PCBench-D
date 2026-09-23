# 一、突变情况分析

- **Total**: 4807
- **替代API**: `matplotlib.figure.Figure.draw_without_rendering`
- **10% 阈值**: 480.7

## Vi-1 (v3.5.3-v3.8.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1949 | 0.1901 |
| tokenBased | 2573 | 0.0939 |
| treeBased | 2685 | 0.1542 |

## Vi (v3.6.0-v3.8.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1223 | 0.5690 |
| tokenBased | 149 | 0.2727 |
| treeBased | 1009 | 0.5526 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1949 | 1223 | +726 | true |
| tokenBased | 2573 | 149 | +2424 | true |
| treeBased | 2685 | 1009 | +1676 | true |

```json
{
  "total": 4807,
  "replacement_api": "matplotlib.figure.Figure.draw_without_rendering",
  "threshold_10pct": 480.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1949,
      "score": 0.190083
    },
    "tokenBased": {
      "rank": 2573,
      "score": 0.093923
    },
    "treeBased": {
      "rank": 2685,
      "score": 0.154185
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1223,
      "score": 0.569
    },
    "tokenBased": {
      "rank": 149,
      "score": 0.272727
    },
    "treeBased": {
      "rank": 1009,
      "score": 0.552632
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1949,
      "vi_rank": 1223,
      "delta": 726,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2573,
      "vi_rank": 149,
      "delta": 2424,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2685,
      "vi_rank": 1009,
      "delta": 1676,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.colorbar.Colorbar.draw_all/Vi-1_v3.5.3.py`
- **new**: `matplotlib.colorbar.Colorbar.draw_all/Vi_v3.6.0.py`
- **+2 / -46**

```diff
--- matplotlib.colorbar.Colorbar.draw_all/Vi-1_v3.5.3.py
+++ matplotlib.colorbar.Colorbar.draw_all/Vi_v3.6.0.py
@@ -1,48 +1,4 @@
+    @_api.deprecated("3.6", alternative="fig.draw_without_rendering()")
     def draw_all(self):
         
-        if self.orientation == 'vertical':
-            if mpl.rcParams['ytick.minor.visible']:
-                self.minorticks_on()
-        else:
-            if mpl.rcParams['xtick.minor.visible']:
-                self.minorticks_on()
-        self._long_axis().set(label_position=self.ticklocation,
-                              ticks_position=self.ticklocation)
-        self._short_axis().set_ticks([])
-        self._short_axis().set_ticks([], minor=True)
-
-
-
-
-
-        self._process_values()
-
-
-        self.vmin, self.vmax = self._boundaries[self._inside][[0, -1]]
-
-        X, Y = self._mesh()
-
-
-        self._do_extends()
-        lower, upper = self.vmin, self.vmax
-        if self._long_axis().get_inverted():
-
-            lower, upper = upper, lower
-        if self.orientation == 'vertical':
-            self.ax.set_xlim(0, 1)
-            self.ax.set_ylim(lower, upper)
-        else:
-            self.ax.set_ylim(0, 1)
-            self.ax.set_xlim(lower, upper)
-
-
-
-        self.update_ticks()
-
-        if self.filled:
-            ind = np.arange(len(self._values))
-            if self._extend_lower():
-                ind = ind[1:]
-            if self._extend_upper():
-                ind = ind[:-1]
-            self._add_solids(X, Y, self._values[ind, np.newaxis])
+        self._draw_all()
```

```json
{
  "old_file": "matplotlib.colorbar.Colorbar.draw_all/Vi-1_v3.5.3.py",
  "new_file": "matplotlib.colorbar.Colorbar.draw_all/Vi_v3.6.0.py",
  "lines_added": 2,
  "lines_removed": 46
}
```
