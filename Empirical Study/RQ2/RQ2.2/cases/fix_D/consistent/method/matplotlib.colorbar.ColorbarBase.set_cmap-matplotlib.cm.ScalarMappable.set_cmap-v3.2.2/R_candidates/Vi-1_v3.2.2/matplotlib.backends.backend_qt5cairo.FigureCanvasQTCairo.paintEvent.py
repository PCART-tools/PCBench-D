    def paintEvent(self, event):
        self._update_dpi()
        dpi_ratio = self._dpi_ratio
        width = int(dpi_ratio * self.width())
        height = int(dpi_ratio * self.height())
        if (width, height) != self._renderer.get_canvas_width_height():
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
            self._renderer.set_ctx_from_surface(surface)
            self._renderer.set_width_height(width, height)
            self.figure.draw(self._renderer)
        buf = self._renderer.gc.ctx.get_target().get_data()
        qimage = QtGui.QImage(buf, width, height,
                              QtGui.QImage.Format_ARGB32_Premultiplied)
        # Adjust the buf reference count to work around a memory leak bug in
        # QImage under PySide on Python 3.
        if QT_API == 'PySide':
            ctypes.c_long.from_address(id(buf)).value = 1
        _setDevicePixelRatioF(qimage, dpi_ratio)
        painter = QtGui.QPainter(self)
        painter.eraseRect(event.rect())
        painter.drawImage(0, 0, qimage)
        self._draw_rect_callback(painter)
        painter.end()
