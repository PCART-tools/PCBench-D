# 一、突变情况分析

- **Total**: 168
- **替代API**: `matplotlib.backends.backend_qt5.FigureCanvasQT`
- **10% 阈值**: 16.8

## Vi-1 (v2.1.2-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 56 | 0.1597 |
| tokenBased | 36 | 0.3632 |

## Vi (v2.2.0-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 64 | 0.0000 |
| tokenBased | 150 | 0.0101 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 56 | 64 | -8 | false |
| tokenBased | 36 | 150 | -114 | true |

```json
{
  "total": 168,
  "replacement_api": "matplotlib.backends.backend_qt5.FigureCanvasQT",
  "threshold_10pct": 16.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 56,
      "score": 0.159746
    },
    "tokenBased": {
      "rank": 36,
      "score": 0.363192
    }
  },
  "vi": {
    "mapBased": {
      "rank": 64,
      "score": 0.0
    },
    "tokenBased": {
      "rank": 150,
      "score": 0.010135
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 56,
      "vi_rank": 64,
      "delta": -8,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 36,
      "vi_rank": 150,
      "delta": -114,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.backends.backend_qt5agg.FigureCanvasQTAggBase/Vi-1_v2.1.2.py`
- **new**: `matplotlib.backends.backend_qt5agg.FigureCanvasQTAggBase/Vi_v2.2.0.py`
- **+3 / -149**

```diff
--- matplotlib.backends.backend_qt5agg.FigureCanvasQTAggBase/Vi-1_v2.1.2.py
+++ matplotlib.backends.backend_qt5agg.FigureCanvasQTAggBase/Vi_v2.2.0.py
@@ -1,149 +1,3 @@
-class FigureCanvasQTAggBase(FigureCanvasAgg):
-    
-
-    def __init__(self, figure):
-        super(FigureCanvasQTAggBase, self).__init__(figure=figure)
-        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
-        self._agg_draw_pending = False
-        self._agg_is_drawing = False
-        self._bbox_queue = []
-        self._drawRect = None
-
-    def drawRectangle(self, rect):
-        if rect is not None:
-            self._drawRect = [pt / self._dpi_ratio for pt in rect]
-        else:
-            self._drawRect = None
-        self.update()
-
-    @property
-    @cbook.deprecated("2.1")
-    def blitbox(self):
-        return self._bbox_queue
-
-    def paintEvent(self, e):
-        
-
-
-        if self._agg_draw_pending:
-            self.__draw_idle_agg()
-
-
-
-        if self._dpi_ratio != self._dpi_ratio_prev:
-
-            self._update_figure_dpi()
-            self._dpi_ratio_prev = self._dpi_ratio
-
-
-
-            event = QtGui.QResizeEvent(self.size(), self.size())
-
-
-
-            self.resizeEvent(event)
-
-            return
-
-
-
-        if not hasattr(self, 'renderer'):
-            return
-
-        painter = QtGui.QPainter(self)
-
-        if self._bbox_queue:
-            bbox_queue = self._bbox_queue
-        else:
-            painter.eraseRect(self.rect())
-            bbox_queue = [
-                Bbox([[0, 0], [self.renderer.width, self.renderer.height]])]
-        self._bbox_queue = []
-        for bbox in bbox_queue:
-            l, b, r, t = map(int, bbox.extents)
-            w = r - l
-            h = t - b
-            reg = self.copy_from_bbox(bbox)
-            buf = reg.to_string_argb()
-            qimage = QtGui.QImage(buf, w, h, QtGui.QImage.Format_ARGB32)
-            if hasattr(qimage, 'setDevicePixelRatio'):
-
-                qimage.setDevicePixelRatio(self._dpi_ratio)
-            origin = QtCore.QPoint(l, self.renderer.height - t)
-            painter.drawImage(origin / self._dpi_ratio, qimage)
-
-
-            if QT_API == 'PySide' and six.PY3:
-                ctypes.c_long.from_address(id(buf)).value = 1
-
-
-        if self._drawRect is not None:
-            pen = QtGui.QPen(QtCore.Qt.black, 1 / self._dpi_ratio,
-                             QtCore.Qt.DotLine)
-            painter.setPen(pen)
-            x, y, w, h = self._drawRect
-            painter.drawRect(x, y, w, h)
-
-        painter.end()
-
-    def draw(self):
-        
-
-
-        if self._agg_is_drawing:
-            return
-
-        self._agg_is_drawing = True
-        try:
-            super(FigureCanvasQTAggBase, self).draw()
-        finally:
-            self._agg_is_drawing = False
-        self.update()
-
-    def draw_idle(self):
-        
-
-
-
-
-
-        if not (self._agg_draw_pending or self._agg_is_drawing):
-            self._agg_draw_pending = True
-            QtCore.QTimer.singleShot(0, self.__draw_idle_agg)
-
-    def __draw_idle_agg(self, *args):
-
-        if not self._agg_draw_pending:
-            return
-
-
-
-
-        self._agg_draw_pending = False
-
-        if self.height() < 0 or self.width() < 0:
-            return
-        try:
-
-            self.draw()
-        except Exception:
-
-            traceback.print_exc()
-
-    def blit(self, bbox=None):
-        
-
-
-        if bbox is None and self.figure:
-            bbox = self.figure.bbox
-
-        self._bbox_queue.append(bbox)
-
-
-        l, b, w, h = [pt / self._dpi_ratio for pt in bbox.bounds]
-        t = b + h
-        self.repaint(l, self.renderer.height / self._dpi_ratio - t, w, h)
-
-    def print_figure(self, *args, **kwargs):
-        super(FigureCanvasQTAggBase, self).print_figure(*args, **kwargs)
-        self.draw()
+@cbook.deprecated("2.2")
+class FigureCanvasQTAggBase(FigureCanvasQTAgg):
+    pass
```

```json
{
  "old_file": "matplotlib.backends.backend_qt5agg.FigureCanvasQTAggBase/Vi-1_v2.1.2.py",
  "new_file": "matplotlib.backends.backend_qt5agg.FigureCanvasQTAggBase/Vi_v2.2.0.py",
  "lines_added": 3,
  "lines_removed": 149
}
```
