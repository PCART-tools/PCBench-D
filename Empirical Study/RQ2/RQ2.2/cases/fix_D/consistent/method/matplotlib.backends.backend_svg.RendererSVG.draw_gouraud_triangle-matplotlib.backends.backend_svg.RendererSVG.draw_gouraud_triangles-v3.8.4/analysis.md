# 一、突变情况分析

- **Total**: 804
- **替代API**: `matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangles`
- **10% 阈值**: 80.4

## Vi-1 (v3.6.3-v3.8.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 207 | 0.1798 |
| tokenBased | 220 | 0.1087 |
| treeBased | 240 | 0.1409 |

## Vi (v3.6.3-v3.9.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.4323 |
| tokenBased | 76 | 0.2506 |
| treeBased | 52 | 0.3190 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 207 | 1 | +206 | true |
| tokenBased | 220 | 76 | +144 | true |
| treeBased | 240 | 52 | +188 | true |

```json
{
  "total": 804,
  "replacement_api": "matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangles",
  "threshold_10pct": 80.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 207,
      "score": 0.179794
    },
    "tokenBased": {
      "rank": 220,
      "score": 0.108747
    },
    "treeBased": {
      "rank": 240,
      "score": 0.1409
    }
  },
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 207,
      "vi_rank": 1,
      "delta": 206,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 220,
      "vi_rank": 76,
      "delta": 144,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 240,
      "vi_rank": 52,
      "delta": 188,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v3.8.4/matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangles.py`
- **new**: `R_candidates/Vi_v3.9.0/matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangles.py`
- **+29 / -4**

```diff
--- R_candidates/Vi-1_v3.8.4/matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangles.py
+++ R_candidates/Vi_v3.9.0/matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangles.py
@@ -1,7 +1,32 @@
     def draw_gouraud_triangles(self, gc, triangles_array, colors_array,
                                transform):
-        self.writer.start('g', **self._get_clip_attrs(gc))
+        writer = self.writer
+        writer.start('g', **self._get_clip_attrs(gc))
         transform = transform.frozen()
-        for tri, col in zip(triangles_array, colors_array):
-            self._draw_gouraud_triangle(gc, tri, col, transform)
-        self.writer.end('g')
+        trans_and_flip = self._make_flip_transform(transform)
+
+        if not self._has_gouraud:
+            self._has_gouraud = True
+            writer.start(
+                'filter',
+                id='colorAdd')
+            writer.element(
+                'feComposite',
+                attrib={'in': 'SourceGraphic'},
+                in2='BackgroundImage',
+                operator='arithmetic',
+                k2="1", k3="1")
+            writer.end('filter')
+
+            writer.start(
+                'filter',
+                id='colorMat')
+            writer.element(
+                'feColorMatrix',
+                attrib={'type': 'matrix'},
+                values='1 0 0 0 0 \n0 1 0 0 0 \n0 0 1 0 0 \n1 1 1 1 0 \n0 0 0 0 1 ')
+            writer.end('filter')
+
+        for points, colors in zip(triangles_array, colors_array):
+            self._draw_gouraud_triangle(trans_and_flip.transform(points), colors)
+        writer.end('g')
```

```json
{
  "old_file": "R_candidates/Vi-1_v3.8.4/matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangles.py",
  "new_file": "R_candidates/Vi_v3.9.0/matplotlib.backends.backend_svg.RendererSVG.draw_gouraud_triangles.py",
  "lines_added": 29,
  "lines_removed": 4
}
```
