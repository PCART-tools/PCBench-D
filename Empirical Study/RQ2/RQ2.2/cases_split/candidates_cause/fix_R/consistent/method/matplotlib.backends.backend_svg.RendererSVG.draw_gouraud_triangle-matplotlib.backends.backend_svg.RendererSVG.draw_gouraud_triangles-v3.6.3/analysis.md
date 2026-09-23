# 一、突变情况分析

- **Total**: 812
- **替代API**: `matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangles`
- **10% 阈值**: 81.2

## Vi-1 (v3.6.3-v3.9.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.4323 |
| tokenBased | 76 | 0.2506 |
| treeBased | 52 | 0.3190 |

## Vi (v3.7.0-v3.9.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 528 | 0.3135 |
| tokenBased | 398 | 0.1810 |
| treeBased | 671 | 0.2158 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 528 | -527 | true |
| tokenBased | 76 | 398 | -322 | true |
| treeBased | 52 | 671 | -619 | true |

```json
{
  "total": 812,
  "replacement_api": "matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangles",
  "threshold_10pct": 81.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.432334
    },
    "tokenBased": {
      "rank": 76,
      "score": 0.250591
    },
    "treeBased": {
      "rank": 52,
      "score": 0.319039
    }
  },
  "vi": {
    "mapBased": {
      "rank": 528,
      "score": 0.313459
    },
    "tokenBased": {
      "rank": 398,
      "score": 0.181034
    },
    "treeBased": {
      "rank": 671,
      "score": 0.215827
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 528,
      "delta": -527,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 76,
      "vi_rank": 398,
      "delta": -322,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 52,
      "vi_rank": 671,
      "delta": -619,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangle/Vi-1_v3.6.3.py`
- **new**: `matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangle/Vi_v3.7.0.py`
- **+1 / -129**

```diff
--- matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangle/Vi-1_v3.6.3.py
+++ matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangle/Vi_v3.7.0.py
@@ -1,131 +1,3 @@
     def draw_gouraud_triangle(self, gc, points, colors, trans):
 
-
-
-
-
-
-
-
-
-
-
-
-
-        writer = self.writer
-        if not self._has_gouraud:
-            self._has_gouraud = True
-            writer.start(
-                'filter',
-                id='colorAdd')
-            writer.element(
-                'feComposite',
-                attrib={'in': 'SourceGraphic'},
-                in2='BackgroundImage',
-                operator='arithmetic',
-                k2="1", k3="1")
-            writer.end('filter')
-
-            writer.start(
-                'filter',
-                id='colorMat')
-            writer.element(
-                'feColorMatrix',
-                attrib={'type': 'matrix'},
-                values='1 0 0 0 0 \n0 1 0 0 0 \n0 0 1 0 0' +
-                       ' \n1 1 1 1 0 \n0 0 0 0 1 ')
-            writer.end('filter')
-
-        avg_color = np.average(colors, axis=0)
-        if avg_color[-1] == 0:
-
-            return
-
-        trans_and_flip = self._make_flip_transform(trans)
-        tpoints = trans_and_flip.transform(points)
-
-        writer.start('defs')
-        for i in range(3):
-            x1, y1 = tpoints[i]
-            x2, y2 = tpoints[(i + 1) % 3]
-            x3, y3 = tpoints[(i + 2) % 3]
-            rgba_color = colors[i]
-
-            if x2 == x3:
-                xb = x2
-                yb = y1
-            elif y2 == y3:
-                xb = x1
-                yb = y2
-            else:
-                m1 = (y2 - y3) / (x2 - x3)
-                b1 = y2 - (m1 * x2)
-                m2 = -(1.0 / m1)
-                b2 = y1 - (m2 * x1)
-                xb = (-b1 + b2) / (m1 - m2)
-                yb = m2 * xb + b2
-
-            writer.start(
-                'linearGradient',
-                id="GR%x_%d" % (self._n_gradients, i),
-                gradientUnits="userSpaceOnUse",
-                x1=_short_float_fmt(x1), y1=_short_float_fmt(y1),
-                x2=_short_float_fmt(xb), y2=_short_float_fmt(yb))
-            writer.element(
-                'stop',
-                offset='1',
-                style=_generate_css({
-                    'stop-color': rgb2hex(avg_color),
-                    'stop-opacity': _short_float_fmt(rgba_color[-1])}))
-            writer.element(
-                'stop',
-                offset='0',
-                style=_generate_css({'stop-color': rgb2hex(rgba_color),
-                                    'stop-opacity': "0"}))
-
-            writer.end('linearGradient')
-
-        writer.end('defs')
-
-
-        dpath = "M " + _short_float_fmt(x1)+',' + _short_float_fmt(y1)
-        dpath += " L " + _short_float_fmt(x2) + ',' + _short_float_fmt(y2)
-        dpath += " " + _short_float_fmt(x3) + ',' + _short_float_fmt(y3) + " Z"
-
-        writer.element(
-            'path',
-            attrib={'d': dpath,
-                    'fill': rgb2hex(avg_color),
-                    'fill-opacity': '1',
-                    'shape-rendering': "crispEdges"})
-
-        writer.start(
-                'g',
-                attrib={'stroke': "none",
-                        'stroke-width': "0",
-                        'shape-rendering': "crispEdges",
-                        'filter': "url(#colorMat)"})
-
-        writer.element(
-            'path',
-            attrib={'d': dpath,
-                    'fill': 'url(#GR%x_0)' % self._n_gradients,
-                    'shape-rendering': "crispEdges"})
-
-        writer.element(
-            'path',
-            attrib={'d': dpath,
-                    'fill': 'url(#GR%x_1)' % self._n_gradients,
-                    'filter': 'url(#colorAdd)',
-                    'shape-rendering': "crispEdges"})
-
-        writer.element(
-            'path',
-            attrib={'d': dpath,
-                    'fill': 'url(#GR%x_2)' % self._n_gradients,
-                    'filter': 'url(#colorAdd)',
-                    'shape-rendering': "crispEdges"})
-
-        writer.end('g')
-
-        self._n_gradients += 1
+        self._draw_gouraud_triangle(gc, points, colors, trans)
```

```json
{
  "old_file": "matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangle/Vi-1_v3.6.3.py",
  "new_file": "matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangle/Vi_v3.7.0.py",
  "lines_added": 1,
  "lines_removed": 129
}
```
