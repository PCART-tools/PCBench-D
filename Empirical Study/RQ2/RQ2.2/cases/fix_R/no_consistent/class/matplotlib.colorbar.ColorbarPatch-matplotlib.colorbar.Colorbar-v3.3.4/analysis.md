# 一、突变情况分析

- **Total**: 854
- **替代API**: `matplotlib.colorbar.Colorbar`
- **10% 阈值**: 85.4

## Vi-1 (v3.3.4-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 705 | 0.0311 |
| tokenBased | 739 | 0.0612 |

## Vi (v3.4.0-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 265 | 0.0000 |
| tokenBased | 838 | 0.0024 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 705 | 265 | +440 | true |
| tokenBased | 739 | 838 | -99 | true |

```json
{
  "total": 854,
  "replacement_api": "matplotlib.colorbar.Colorbar",
  "threshold_10pct": 85.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 705,
      "score": 0.031097
    },
    "tokenBased": {
      "rank": 739,
      "score": 0.061203
    }
  },
  "vi": {
    "mapBased": {
      "rank": 265,
      "score": 0.0
    },
    "tokenBased": {
      "rank": 838,
      "score": 0.002366
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 705,
      "vi_rank": 265,
      "delta": 440,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 739,
      "vi_rank": 838,
      "delta": -99,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.colorbar.ColorbarPatch/Vi-1_v3.3.4.py`
- **new**: `matplotlib.colorbar.ColorbarPatch/Vi_v3.4.0.py`
- **+2 / -53**

```diff
--- matplotlib.colorbar.ColorbarPatch/Vi-1_v3.3.4.py
+++ matplotlib.colorbar.ColorbarPatch/Vi_v3.4.0.py
@@ -1,54 +1,3 @@
+@_api.deprecated("3.4", alternative="Colorbar")
 class ColorbarPatch(Colorbar):
-    
-
-    def __init__(self, ax, mappable, **kw):
-
-
-
-        self.solids_patches = []
-        Colorbar.__init__(self, ax, mappable, **kw)
-
-    def _add_solids(self, X, Y, C):
-        
-        n_segments = len(C)
-
-
-        hatches = self.mappable.hatches * n_segments
-
-        patches = []
-        for i in range(len(X) - 1):
-            val = C[i][0]
-            hatch = hatches[i]
-
-            xy = np.array([[X[i][0], Y[i][0]],
-                           [X[i][1], Y[i][0]],
-                           [X[i + 1][1], Y[i + 1][0]],
-                           [X[i + 1][0], Y[i + 1][1]]])
-
-            if self.orientation == 'horizontal':
-
-                xy = xy[..., ::-1]
-
-            patch = mpatches.PathPatch(mpath.Path(xy),
-                                       facecolor=self.cmap(self.norm(val)),
-                                       hatch=hatch, linewidth=0,
-                                       antialiased=False, alpha=self.alpha)
-            self.ax.add_patch(patch)
-            patches.append(patch)
-
-        if self.solids_patches:
-            for solid in self.solids_patches:
-                solid.remove()
-
-        self.solids_patches = patches
-
-        if self.dividers is not None:
-            self.dividers.remove()
-            self.dividers = None
-
-        if self.drawedges:
-            self.dividers = collections.LineCollection(
-                    self._edges(X, Y),
-                    colors=(mpl.rcParams['axes.edgecolor'],),
-                    linewidths=(0.5 * mpl.rcParams['axes.linewidth'],))
-            self.ax.add_collection(self.dividers)
+    pass
```

```json
{
  "old_file": "matplotlib.colorbar.ColorbarPatch/Vi-1_v3.3.4.py",
  "new_file": "matplotlib.colorbar.ColorbarPatch/Vi_v3.4.0.py",
  "lines_added": 2,
  "lines_removed": 53
}
```
