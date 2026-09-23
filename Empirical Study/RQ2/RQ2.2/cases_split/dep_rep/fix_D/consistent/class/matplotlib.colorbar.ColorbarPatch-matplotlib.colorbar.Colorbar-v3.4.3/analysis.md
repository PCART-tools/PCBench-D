# 一、突变情况分析

- **Total**: 829
- **替代API**: `matplotlib.colorbar.Colorbar`
- **10% 阈值**: 82.9

## Vi-1 (v3.3.4-v3.4.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 484 | 0.1012 |
| tokenBased | 251 | 0.3173 |

## Vi (v3.3.4-v3.5.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 687 | 0.0353 |
| tokenBased | 723 | 0.0663 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 484 | 687 | -203 | true |
| tokenBased | 251 | 723 | -472 | true |

```json
{
  "total": 829,
  "replacement_api": "matplotlib.colorbar.Colorbar",
  "threshold_10pct": 82.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 484,
      "score": 0.101151
    },
    "tokenBased": {
      "rank": 251,
      "score": 0.317254
    }
  },
  "vi": {
    "mapBased": {
      "rank": 687,
      "score": 0.035331
    },
    "tokenBased": {
      "rank": 723,
      "score": 0.066325
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 484,
      "vi_rank": 687,
      "delta": -203,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 251,
      "vi_rank": 723,
      "delta": -472,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v3.4.3/matplotlib.colorbar.Colorbar.py`
- **new**: `R_candidates/Vi_v3.5.0/matplotlib.colorbar.Colorbar.py`
- **+732 / -74**

```diff
--- R_candidates/Vi-1_v3.4.3/matplotlib.colorbar.Colorbar.py
+++ R_candidates/Vi_v3.5.0/matplotlib.colorbar.Colorbar.py
@@ -1,55 +1,162 @@
-class Colorbar(ColorbarBase):
+class Colorbar:
     
 
-    def __init__(self, ax, mappable, **kwargs):
+    n_rasterize = 50
+
+    def __init__(self, ax, mappable=None, *, cmap=None,
+                 norm=None,
+                 alpha=None,
+                 values=None,
+                 boundaries=None,
+                 orientation='vertical',
+                 ticklocation='auto',
+                 extend=None,
+                 spacing='uniform',
+                 ticks=None,
+                 format=None,
+                 drawedges=False,
+                 filled=True,
+                 extendfrac=None,
+                 extendrect=False,
+                 label='',
+                 ):
+
+        if mappable is None:
+            mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
+
 
 
         if mappable.get_array() is not None:
             mappable.autoscale_None()
 
         self.mappable = mappable
-        _add_disjoint_kwargs(kwargs, cmap=mappable.cmap, norm=mappable.norm)
+        cmap = mappable.cmap
+        norm = mappable.norm
 
         if isinstance(mappable, contour.ContourSet):
             cs = mappable
-            _add_disjoint_kwargs(
-                kwargs,
-                alpha=cs.get_alpha(),
-                boundaries=cs._levels,
-                values=cs.cvalues,
-                extend=cs.extend,
-                filled=cs.filled,
-            )
-            kwargs.setdefault(
-                'ticks', ticker.FixedLocator(cs.levels, nbins=10))
-            super().__init__(ax, **kwargs)
-            if not cs.filled:
-                self.add_lines(cs)
-        else:
-            if getattr(mappable.cmap, 'colorbar_extend', False) is not False:
-                kwargs.setdefault('extend', mappable.cmap.colorbar_extend)
-            if isinstance(mappable, martist.Artist):
-                _add_disjoint_kwargs(kwargs, alpha=mappable.get_alpha())
-            super().__init__(ax, **kwargs)
+            alpha = cs.get_alpha()
+            boundaries = cs._levels
+            values = cs.cvalues
+            extend = cs.extend
+            filled = cs.filled
+            if ticks is None:
+                ticks = ticker.FixedLocator(cs.levels, nbins=10)
+        elif isinstance(mappable, martist.Artist):
+            alpha = mappable.get_alpha()
 
         mappable.colorbar = self
-        mappable.colorbar_cid = mappable.callbacksSM.connect(
+        mappable.colorbar_cid = mappable.callbacks.connect(
             'changed', self.update_normal)
 
-    @_api.deprecated("3.3", alternative="update_normal")
-    def on_mappable_changed(self, mappable):
-        
-        _log.debug('colorbar mappable changed')
-        self.update_normal(mappable)
-
-    def add_lines(self, CS, erase=True):
-        
-        if not isinstance(CS, contour.ContourSet) or CS.filled:
-            raise ValueError('add_lines is only for a ContourSet of lines')
-        tcolors = [c[0] for c in CS.tcolors]
-        tlinewidths = [t[0] for t in CS.tlinewidths]
-
-        super().add_lines(CS.levels, tcolors, tlinewidths, erase=erase)
+        _api.check_in_list(
+            ['vertical', 'horizontal'], orientation=orientation)
+        _api.check_in_list(
+            ['auto', 'left', 'right', 'top', 'bottom'],
+            ticklocation=ticklocation)
+        _api.check_in_list(
+            ['uniform', 'proportional'], spacing=spacing)
+
+        self.ax = ax
+        self.ax._axes_locator = _ColorbarAxesLocator(self)
+
+        if extend is None:
+            if (not isinstance(mappable, contour.ContourSet)
+                    and getattr(cmap, 'colorbar_extend', False) is not False):
+                extend = cmap.colorbar_extend
+            elif hasattr(norm, 'extend'):
+                extend = norm.extend
+            else:
+                extend = 'neither'
+        self.alpha = None
+
+        self.set_alpha(alpha)
+        self.cmap = cmap
+        self.norm = norm
+        self.values = values
+        self.boundaries = boundaries
+        self.extend = extend
+        self._inside = _api.check_getitem(
+            {'neither': slice(0, None), 'both': slice(1, -1),
+             'min': slice(1, None), 'max': slice(0, -1)},
+            extend=extend)
+        self.spacing = spacing
+        self.orientation = orientation
+        self.drawedges = drawedges
+        self.filled = filled
+        self.extendfrac = extendfrac
+        self.extendrect = extendrect
+        self.solids = None
+        self.solids_patches = []
+        self.lines = []
+
+        for spine in self.ax.spines.values():
+            spine.set_visible(False)
+        self.outline = self.ax.spines['outline'] = _ColorbarSpine(self.ax)
+        self._short_axis().set_visible(False)
+
+        self._patch = mpatches.Polygon(
+            np.empty((0, 2)),
+            color=mpl.rcParams['axes.facecolor'], linewidth=0.01, zorder=-1)
+        ax.add_artist(self._patch)
+
+        self.dividers = collections.LineCollection(
+            [],
+            colors=[mpl.rcParams['axes.edgecolor']],
+            linewidths=[0.5 * mpl.rcParams['axes.linewidth']])
+        self.ax.add_collection(self.dividers)
+
+        self.locator = None
+        self.minorlocator = None
+        self.formatter = None
+        self.__scale = None
+
+        if ticklocation == 'auto':
+            ticklocation = 'bottom' if orientation == 'horizontal' else 'right'
+        self.ticklocation = ticklocation
+
+        self.set_label(label)
+        self._reset_locator_formatter_scale()
+
+        if np.iterable(ticks):
+            self.locator = ticker.FixedLocator(ticks, nbins=len(ticks))
+        else:
+            self.locator = ticks
+
+        if isinstance(format, str):
+            self.formatter = ticker.FormatStrFormatter(format)
+        else:
+            self.formatter = format
+        self.draw_all()
+
+        if isinstance(mappable, contour.ContourSet) and not mappable.filled:
+            self.add_lines(mappable)
+
+
+        self.ax._colorbar = self
+
+        if (isinstance(self.norm, (colors.BoundaryNorm, colors.NoNorm)) or
+                isinstance(self.mappable, contour.ContourSet)):
+            self.ax.set_navigate(False)
+
+
+        self._interactive_funcs = ["_get_view", "_set_view",
+                                   "_set_view_from_bbox", "drag_pan"]
+        for x in self._interactive_funcs:
+            setattr(self.ax, x, getattr(self, x))
+
+        self.ax.cla = self._cbar_cla
+
+    def _cbar_cla(self):
+        
+        for x in self._interactive_funcs:
+            delattr(self.ax, x)
+
+        del self.ax.cla
+        self.ax.cla()
+
+
+    patch = _api.deprecate_privatize_attribute("3.5", alternative="ax")
 
     def update_normal(self, mappable):
         
@@ -68,45 +175,335 @@
                 self.add_lines(CS)
         self.stale = True
 
-    @_api.deprecated("3.3", alternative="update_normal")
-    def update_bruteforce(self, mappable):
-        
-
-
-
-
-        self.ax.cla()
-        self.locator = None
-        self.formatter = None
-
-
-        for spine in self.ax.spines.values():
-            spine.set_visible(False)
-        self.outline = self.ax.spines['outline'] = _ColorbarSpine(self.ax)
-        self.patch = mpatches.Polygon(
-            np.empty((0, 2)),
-            color=mpl.rcParams['axes.facecolor'], linewidth=0.01, zorder=-1)
-        self.ax.add_artist(self.patch)
-        self.solids = None
-        self.lines = []
-        self.update_normal(mappable)
-        self.draw_all()
-        if isinstance(self.mappable, contour.ContourSet):
-            CS = self.mappable
-            if not CS.filled:
-                self.add_lines(CS)
-
-
-
-
-
-
-
+    def draw_all(self):
+        
+        if self.orientation == 'vertical':
+            if mpl.rcParams['ytick.minor.visible']:
+                self.minorticks_on()
+        else:
+            if mpl.rcParams['xtick.minor.visible']:
+                self.minorticks_on()
+        self._long_axis().set(label_position=self.ticklocation,
+                              ticks_position=self.ticklocation)
+        self._short_axis().set_ticks([])
+        self._short_axis().set_ticks([], minor=True)
+
+
+
+
+
+        self._process_values()
+
+
+        self.vmin, self.vmax = self._boundaries[self._inside][[0, -1]]
+
+        X, Y, extendlen = self._mesh()
+
+
+        self._do_extends(extendlen)
+
+        if self.orientation == 'vertical':
+            self.ax.set_xlim(0, 1)
+            self.ax.set_ylim(self.vmin, self.vmax)
+        else:
+            self.ax.set_ylim(0, 1)
+            self.ax.set_xlim(self.vmin, self.vmax)
+
+
+
+        self.update_ticks()
+
+        if self.filled:
+            ind = np.arange(len(self._values))
+            if self._extend_lower():
+                ind = ind[1:]
+            if self._extend_upper():
+                ind = ind[:-1]
+            self._add_solids(X, Y, self._values[ind, np.newaxis])
+
+    def _add_solids(self, X, Y, C):
+        
+
+        if self.solids is not None:
+            self.solids.remove()
+        for solid in self.solids_patches:
+            solid.remove()
+
+
+        mappable = getattr(self, 'mappable', None)
+        if (isinstance(mappable, contour.ContourSet)
+                and any(hatch is not None for hatch in mappable.hatches)):
+            self._add_solids_patches(X, Y, C, mappable)
+        else:
+            self.solids = self.ax.pcolormesh(
+                X, Y, C, cmap=self.cmap, norm=self.norm, alpha=self.alpha,
+                edgecolors='none', shading='flat')
+            if not self.drawedges:
+                if len(self._y) >= self.n_rasterize:
+                    self.solids.set_rasterized(True)
+        self.dividers.set_segments(
+            np.dstack([X, Y])[1:-1] if self.drawedges else [])
+
+    def _add_solids_patches(self, X, Y, C, mappable):
+        hatches = mappable.hatches * len(C)
+        patches = []
+        for i in range(len(X) - 1):
+            xy = np.array([[X[i, 0], Y[i, 0]],
+                           [X[i, 1], Y[i, 0]],
+                           [X[i + 1, 1], Y[i + 1, 0]],
+                           [X[i + 1, 0], Y[i + 1, 1]]])
+            patch = mpatches.PathPatch(mpath.Path(xy),
+                                       facecolor=self.cmap(self.norm(C[i][0])),
+                                       hatch=hatches[i], linewidth=0,
+                                       antialiased=False, alpha=self.alpha)
+            self.ax.add_patch(patch)
+            patches.append(patch)
+        self.solids_patches = patches
+
+    def _do_extends(self, extendlen):
+        
+
+
+        bot = 0 - (extendlen[0] if self._extend_lower() else 0)
+        top = 1 + (extendlen[1] if self._extend_upper() else 0)
+
+
+        if not self.extendrect:
+
+            xyout = np.array([[0, 0], [0.5, bot], [1, 0],
+                              [1, 1], [0.5, top], [0, 1], [0, 0]])
+        else:
+
+            xyout = np.array([[0, 0], [0, bot], [1, bot], [1, 0],
+                              [1, 1], [1, top], [0, top], [0, 1],
+                              [0, 0]])
+
+        if self.orientation == 'horizontal':
+            xyout = xyout[:, ::-1]
+
+
+        self.outline.set_xy(xyout)
+        if not self.filled:
+            return
+
+
+
+        mappable = getattr(self, 'mappable', None)
+        if (isinstance(mappable, contour.ContourSet)
+                and any(hatch is not None for hatch in mappable.hatches)):
+            hatches = mappable.hatches
+        else:
+            hatches = [None]
+
+        if self._extend_lower():
+            if not self.extendrect:
+
+                xy = np.array([[0, 0], [0.5, bot], [1, 0]])
+            else:
+
+                xy = np.array([[0, 0], [0, bot], [1., bot], [1, 0]])
+            if self.orientation == 'horizontal':
+                xy = xy[:, ::-1]
+
+            color = self.cmap(self.norm(self._values[0]))
+            patch = mpatches.PathPatch(
+                mpath.Path(xy), facecolor=color, linewidth=0,
+                antialiased=False, transform=self.ax.transAxes,
+                hatch=hatches[0], clip_on=False)
+            self.ax.add_patch(patch)
+        if self._extend_upper():
+            if not self.extendrect:
+
+                xy = np.array([[0, 1], [0.5, top], [1, 1]])
+            else:
+
+                xy = np.array([[0, 1], [0, top], [1, top], [1, 1]])
+            if self.orientation == 'horizontal':
+                xy = xy[:, ::-1]
+
+            color = self.cmap(self.norm(self._values[-1]))
+            patch = mpatches.PathPatch(
+                mpath.Path(xy), facecolor=color,
+                linewidth=0, antialiased=False,
+                transform=self.ax.transAxes, hatch=hatches[-1], clip_on=False)
+            self.ax.add_patch(patch)
+        return
+
+    def add_lines(self, *args, **kwargs):
+        
+        params = _api.select_matching_signature(
+            [lambda self, CS, erase=True: locals(),
+             lambda self, levels, colors, linewidths, erase=True: locals()],
+            self, *args, **kwargs)
+        if "CS" in params:
+            self, CS, erase = params.values()
+            if not isinstance(CS, contour.ContourSet) or CS.filled:
+                raise ValueError("If a single artist is passed to add_lines, "
+                                 "it must be a ContourSet of lines")
+
+            return self.add_lines(
+                CS.levels,
+                [c[0] for c in CS.tcolors],
+                [t[0] for t in CS.tlinewidths],
+                erase=erase)
+        else:
+            self, levels, colors, linewidths, erase = params.values()
+
+        y = self._locate(levels)
+        rtol = (self._y[-1] - self._y[0]) * 1e-10
+        igood = (y < self._y[-1] + rtol) & (y > self._y[0] - rtol)
+        y = y[igood]
+        if np.iterable(colors):
+            colors = np.asarray(colors)[igood]
+        if np.iterable(linewidths):
+            linewidths = np.asarray(linewidths)[igood]
+        X, Y = np.meshgrid([0, 1], y)
+        if self.orientation == 'vertical':
+            xy = np.stack([X, Y], axis=-1)
+        else:
+            xy = np.stack([Y, X], axis=-1)
+        col = collections.LineCollection(xy, linewidths=linewidths,
+                                         colors=colors)
+
+        if erase and self.lines:
+            for lc in self.lines:
+                lc.remove()
+            self.lines = []
+        self.lines.append(col)
+
+
+        fac = np.max(linewidths) / 72
+        xy = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
+        inches = self.ax.get_figure().dpi_scale_trans
+
+        xy = inches.inverted().transform(self.ax.transAxes.transform(xy))
+        xy[[0, 1, 4], 1] -= fac
+        xy[[2, 3], 1] += fac
+
+        xy = self.ax.transAxes.inverted().transform(inches.transform(xy))
+        if self.orientation == 'horizontal':
+            xy = xy.T
+        col.set_clip_path(mpath.Path(xy, closed=True),
+                          self.ax.transAxes)
+        self.ax.add_collection(col)
+        self.stale = True
+
+    def update_ticks(self):
+        
+
+        self._get_ticker_locator_formatter()
+        self._long_axis().set_major_locator(self.locator)
+        self._long_axis().set_minor_locator(self.minorlocator)
+        self._long_axis().set_major_formatter(self.formatter)
+
+    def _get_ticker_locator_formatter(self):
+        
+        locator = self.locator
+        formatter = self.formatter
+        minorlocator = self.minorlocator
+        if isinstance(self.norm, colors.BoundaryNorm):
+            b = self.norm.boundaries
+            if locator is None:
+                locator = ticker.FixedLocator(b, nbins=10)
+        elif self.boundaries is not None:
+            b = self._boundaries[self._inside]
+            if locator is None:
+                locator = ticker.FixedLocator(b, nbins=10)
+        else:
+            if locator is None:
+
+
+                locator = self._long_axis().get_major_locator()
+            if minorlocator is None:
+                minorlocator = self._long_axis().get_minor_locator()
+            if isinstance(self.norm, colors.NoNorm):
+
+                nv = len(self._values)
+                base = 1 + int(nv / 10)
+                locator = ticker.IndexLocator(base=base, offset=0)
+
+        if minorlocator is None:
+            minorlocator = ticker.NullLocator()
+
+        if formatter is None:
+            formatter = self._long_axis().get_major_formatter()
+
+        self.locator = locator
+        self.formatter = formatter
+        self.minorlocator = minorlocator
+        _log.debug('locator: %r', locator)
+
+    @_api.delete_parameter("3.5", "update_ticks")
+    def set_ticks(self, ticks, update_ticks=True, labels=None, *,
+                  minor=False, **kwargs):
+        
+        if np.iterable(ticks):
+            self._long_axis().set_ticks(ticks, labels=labels, minor=minor,
+                                        **kwargs)
+            self.locator = self._long_axis().get_major_locator()
+        else:
+            self.locator = ticks
+            self._long_axis().set_major_locator(self.locator)
+        self.stale = True
+
+    def get_ticks(self, minor=False):
+        
+        if minor:
+            return self._long_axis().get_minorticklocs()
+        else:
+            return self._long_axis().get_majorticklocs()
+
+    @_api.delete_parameter("3.5", "update_ticks")
+    def set_ticklabels(self, ticklabels, update_ticks=True, *, minor=False,
+                       **kwargs):
+        
+        self._long_axis().set_ticklabels(ticklabels, minor=minor, **kwargs)
+
+    def minorticks_on(self):
+        
+        self.ax.minorticks_on()
+        self.minorlocator = self._long_axis().get_minor_locator()
+        self._short_axis().set_minor_locator(ticker.NullLocator())
+
+    def minorticks_off(self):
+        
+        self.minorlocator = ticker.NullLocator()
+        self._long_axis().set_minor_locator(self.minorlocator)
+
+    def set_label(self, label, *, loc=None, **kwargs):
+        
+        if self.orientation == "vertical":
+            self.ax.set_ylabel(label, loc=loc, **kwargs)
+        else:
+            self.ax.set_xlabel(label, loc=loc, **kwargs)
+        self.stale = True
+
+    def set_alpha(self, alpha):
+        
+        self.alpha = None if isinstance(alpha, np.ndarray) else alpha
+
+    def _set_scale(self, scale, **kwargs):
+        
+        if self.orientation == 'vertical':
+            self.ax.set_yscale(scale, **kwargs)
+        else:
+            self.ax.set_xscale(scale, **kwargs)
+        if isinstance(scale, mscale.ScaleBase):
+            self.__scale = scale.name
+        else:
+            self.__scale = scale
 
     def remove(self):
         
-        super().remove()
-        self.mappable.callbacksSM.disconnect(self.mappable.colorbar_cid)
+        if hasattr(self.ax, '_colorbar_info'):
+            parents = self.ax._colorbar_info['parents']
+            for a in parents:
+                if self.ax in a._colorbars:
+                    a._colorbars.remove(self.ax)
+
+        self.ax.remove()
+
+        self.mappable.callbacks.disconnect(self.mappable.colorbar_cid)
         self.mappable.colorbar = None
         self.mappable.colorbar_cid = None
 
@@ -114,7 +511,6 @@
             ax = self.mappable.axes
         except AttributeError:
             return
-
         try:
             gs = ax.get_subplotspec().get_gridspec()
             subplotspec = gs.get_topmost_subplotspec()
@@ -125,3 +521,265 @@
         else:
 
             ax.set_subplotspec(subplotspec)
+
+    def _ticker(self, locator, formatter):
+        
+        if isinstance(self.norm, colors.NoNorm) and self.boundaries is None:
+            intv = self._values[0], self._values[-1]
+        else:
+            intv = self.vmin, self.vmax
+        locator.create_dummy_axis(minpos=intv[0])
+        locator.axis.set_view_interval(*intv)
+        locator.axis.set_data_interval(*intv)
+        formatter.set_axis(locator.axis)
+
+        b = np.array(locator())
+        if isinstance(locator, ticker.LogLocator):
+            eps = 1e-10
+            b = b[(b <= intv[1] * (1 + eps)) & (b >= intv[0] * (1 - eps))]
+        else:
+            eps = (intv[1] - intv[0]) * 1e-10
+            b = b[(b <= intv[1] + eps) & (b >= intv[0] - eps)]
+        ticks = self._locate(b)
+        ticklabels = formatter.format_ticks(b)
+        offset_string = formatter.get_offset()
+        return ticks, ticklabels, offset_string
+
+    def _process_values(self):
+        
+        if self.values is not None:
+
+            self._values = np.array(self.values)
+            if self.boundaries is None:
+
+                b = np.zeros(len(self.values) + 1)
+                b[1:-1] = 0.5 * (self._values[:-1] + self._values[1:])
+                b[0] = 2.0 * b[1] - b[2]
+                b[-1] = 2.0 * b[-2] - b[-3]
+                self._boundaries = b
+                return
+            self._boundaries = np.array(self.boundaries)
+            return
+
+
+        if isinstance(self.norm, colors.BoundaryNorm):
+            b = self.norm.boundaries
+        else:
+
+            N = self.cmap.N + 1
+            b, _ = self._uniform_y(N)
+
+        if self._extend_lower():
+            b = np.hstack((b[0] - 1, b))
+        if self._extend_upper():
+            b = np.hstack((b, b[-1] + 1))
+
+
+        if not self.norm.scaled():
+            self.norm.vmin = 0
+            self.norm.vmax = 1
+        self.norm.vmin, self.norm.vmax = mtransforms.nonsingular(
+            self.norm.vmin, self.norm.vmax, expander=0.1)
+        if not isinstance(self.norm, colors.BoundaryNorm):
+            b = self.norm.inverse(b)
+
+        self._boundaries = np.asarray(b, dtype=float)
+        self._values = 0.5 * (self._boundaries[:-1] + self._boundaries[1:])
+        if isinstance(self.norm, colors.NoNorm):
+            self._values = (self._values + 0.00001).astype(np.int16)
+
+    def _mesh(self):
+        
+
+
+
+
+        norm = copy.deepcopy(self.norm)
+        norm.vmin = self.vmin
+        norm.vmax = self.vmax
+        x = np.array([0.0, 1.0])
+        y, extendlen = self._proportional_y()
+
+        if (isinstance(norm, (colors.BoundaryNorm, colors.NoNorm)) or
+                (self.__scale == 'manual')):
+
+            dv = self.vmax - self.vmin
+            y = y * dv + self.vmin
+        else:
+            y = norm.inverse(y)
+        self._y = y
+        X, Y = np.meshgrid(x, y)
+        if self.orientation == 'vertical':
+            return (X, Y, extendlen)
+        else:
+            return (Y, X, extendlen)
+
+    def _forward_boundaries(self, x):
+        b = self._boundaries
+        y = np.interp(x, b, np.linspace(0, b[-1], len(b)))
+        eps = (b[-1] - b[0]) * 1e-6
+        y[x < b[0]-eps] = -1
+        y[x > b[-1]+eps] = 2
+        return y
+
+    def _inverse_boundaries(self, x):
+        b = self._boundaries
+        return np.interp(x, np.linspace(0, b[-1], len(b)), b)
+
+    def _reset_locator_formatter_scale(self):
+        
+        self._process_values()
+        self.locator = None
+        self.minorlocator = None
+        self.formatter = None
+        if (self.boundaries is not None or
+                isinstance(self.norm, colors.BoundaryNorm)):
+            if self.spacing == 'uniform':
+                funcs = (self._forward_boundaries, self._inverse_boundaries)
+                self._set_scale('function', functions=funcs)
+            elif self.spacing == 'proportional':
+                self._set_scale('linear')
+        elif hasattr(self.norm, '_scale') and self.norm._scale is not None:
+
+            self._set_scale(self.norm._scale)
+        elif type(self.norm) is colors.Normalize:
+
+            self._set_scale('linear')
+        else:
+
+
+            funcs = (self.norm, self.norm.inverse)
+            self._set_scale('function', functions=funcs)
+
+    def _locate(self, x):
+        
+        if isinstance(self.norm, (colors.NoNorm, colors.BoundaryNorm)):
+            b = self._boundaries
+            xn = x
+        else:
+
+
+            b = self.norm(self._boundaries, clip=False).filled()
+            xn = self.norm(x, clip=False).filled()
+
+        bunique = b[self._inside]
+        yunique = self._y
+
+        z = np.interp(xn, bunique, yunique)
+        return z
+
+
+
+    def _uniform_y(self, N):
+        
+        automin = automax = 1. / (N - 1.)
+        extendlength = self._get_extension_lengths(self.extendfrac,
+                                                   automin, automax,
+                                                   default=0.05)
+        y = np.linspace(0, 1, N)
+        return y, extendlength
+
+    def _proportional_y(self):
+        
+        if isinstance(self.norm, colors.BoundaryNorm):
+            y = (self._boundaries - self._boundaries[self._inside][0])
+            y = y / (self._boundaries[self._inside][-1] -
+                     self._boundaries[self._inside][0])
+
+
+            if self.spacing == 'uniform':
+                yscaled = self._forward_boundaries(self._boundaries)
+            else:
+                yscaled = y
+        else:
+            y = self.norm(self._boundaries.copy())
+            y = np.ma.filled(y, np.nan)
+
+            yscaled = y
+        y = y[self._inside]
+        yscaled = yscaled[self._inside]
+
+        norm = colors.Normalize(y[0], y[-1])
+        y = np.ma.filled(norm(y), np.nan)
+        norm = colors.Normalize(yscaled[0], yscaled[-1])
+        yscaled = np.ma.filled(norm(yscaled), np.nan)
+
+
+        automin = yscaled[1] - yscaled[0]
+        automax = yscaled[-1] - yscaled[-2]
+        extendlength = [0, 0]
+        if self._extend_lower() or self._extend_upper():
+            extendlength = self._get_extension_lengths(
+                    self.extendfrac, automin, automax, default=0.05)
+        return y, extendlength
+
+    def _get_extension_lengths(self, frac, automin, automax, default=0.05):
+        
+
+        extendlength = np.array([default, default])
+        if isinstance(frac, str):
+            _api.check_in_list(['auto'], extendfrac=frac.lower())
+
+            extendlength[:] = [automin, automax]
+        elif frac is not None:
+            try:
+
+                extendlength[:] = frac
+
+
+                if np.isnan(extendlength).any():
+                    raise ValueError()
+            except (TypeError, ValueError) as err:
+
+                raise ValueError('invalid value for extendfrac') from err
+        return extendlength
+
+    def _extend_lower(self):
+        
+        return self.extend in ('both', 'min')
+
+    def _extend_upper(self):
+        
+        return self.extend in ('both', 'max')
+
+    def _long_axis(self):
+        
+        if self.orientation == 'vertical':
+            return self.ax.yaxis
+        return self.ax.xaxis
+
+    def _short_axis(self):
+        
+        if self.orientation == 'vertical':
+            return self.ax.xaxis
+        return self.ax.yaxis
+
+    def _get_view(self):
+
+
+        return self.norm.vmin, self.norm.vmax
+
+    def _set_view(self, view):
+
+
+        self.norm.vmin, self.norm.vmax = view
+
+    def _set_view_from_bbox(self, bbox, direction='in',
+                            mode=None, twinx=False, twiny=False):
+
+
+        new_xbound, new_ybound = self.ax._prepare_view_from_bbox(
+            bbox, direction=direction, mode=mode, twinx=twinx, twiny=twiny)
+        if self.orientation == 'horizontal':
+            self.norm.vmin, self.norm.vmax = new_xbound
+        elif self.orientation == 'vertical':
+            self.norm.vmin, self.norm.vmax = new_ybound
+
+    def drag_pan(self, button, key, x, y):
+
+        points = self.ax._get_pan_points(button, key, x, y)
+        if points is not None:
+            if self.orientation == 'horizontal':
+                self.norm.vmin, self.norm.vmax = points[:, 0]
+            elif self.orientation == 'vertical':
+                self.norm.vmin, self.norm.vmax = points[:, 1]
```

```json
{
  "old_file": "R_candidates/Vi-1_v3.4.3/matplotlib.colorbar.Colorbar.py",
  "new_file": "R_candidates/Vi_v3.5.0/matplotlib.colorbar.Colorbar.py",
  "lines_added": 732,
  "lines_removed": 74
}
```
