    def paintEvent(self, e):
        """Copy the image from the Agg canvas to the qt.drawable.

        In Qt, all drawing should be done inside of here when a widget is
        shown onscreen.
        """
        # if there is a pending draw, run it now as we need the updated render
        # to paint the widget
        if self._agg_draw_pending:
            self.__draw_idle_agg()
        # As described in __init__ above, we need to be careful in cases with
        # mixed resolution displays if dpi_ratio is changing between painting
        # events.
        if self._dpi_ratio != self._dpi_ratio_prev:
            # We need to update the figure DPI
            self._update_figure_dpi()
            self._dpi_ratio_prev = self._dpi_ratio
            # The easiest way to resize the canvas is to emit a resizeEvent
            # since we implement all the logic for resizing the canvas for
            # that event.
            event = QtGui.QResizeEvent(self.size(), self.size())
            # We use self.resizeEvent here instead of QApplication.postEvent
            # since the latter doesn't guarantee that the event will be emitted
            # straight away, and this causes visual delays in the changes.
            self.resizeEvent(event)
            # resizeEvent triggers a paintEvent itself, so we exit this one.
            return

        # if the canvas does not have a renderer, then give up and wait for
        # FigureCanvasAgg.draw(self) to be called
        if not hasattr(self, 'renderer'):
            return

        painter = QtGui.QPainter(self)

        if self._bbox_queue:
            bbox_queue = self._bbox_queue
        else:
            painter.eraseRect(self.rect())
            bbox_queue = [
                Bbox([[0, 0], [self.renderer.width, self.renderer.height]])]
        self._bbox_queue = []
        for bbox in bbox_queue:
            l, b, r, t = map(int, bbox.extents)
            w = r - l
            h = t - b
            reg = self.copy_from_bbox(bbox)
            buf = reg.to_string_argb()
            qimage = QtGui.QImage(buf, w, h, QtGui.QImage.Format_ARGB32)
            if hasattr(qimage, 'setDevicePixelRatio'):
                # Not available on Qt4 or some older Qt5.
                qimage.setDevicePixelRatio(self._dpi_ratio)
            origin = QtCore.QPoint(l, self.renderer.height - t)
            painter.drawImage(origin / self._dpi_ratio, qimage)
            # Adjust the buf reference count to work around a memory
            # leak bug in QImage under PySide on Python 3.
            if QT_API == 'PySide' and six.PY3:
                ctypes.c_long.from_address(id(buf)).value = 1

        # draw the zoom rectangle to the QPainter
        if self._drawRect is not None:
            pen = QtGui.QPen(QtCore.Qt.black, 1 / self._dpi_ratio,
                             QtCore.Qt.DotLine)
            painter.setPen(pen)
            x, y, w, h = self._drawRect
            painter.drawRect(x, y, w, h)

        painter.end()
