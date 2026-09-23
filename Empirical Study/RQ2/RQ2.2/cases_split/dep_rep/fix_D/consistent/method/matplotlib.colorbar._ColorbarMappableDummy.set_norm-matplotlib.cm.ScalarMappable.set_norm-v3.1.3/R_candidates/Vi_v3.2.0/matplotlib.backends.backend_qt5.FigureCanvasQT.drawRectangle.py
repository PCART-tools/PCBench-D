    def drawRectangle(self, rect):
        # Draw the zoom rectangle to the QPainter.  _draw_rect_callback needs
        # to be called at the end of paintEvent.
        if rect is not None:
            def _draw_rect_callback(painter):
                pen = QtGui.QPen(QtCore.Qt.black, 1 / self._dpi_ratio,
                                 QtCore.Qt.DotLine)
                painter.setPen(pen)
                painter.drawRect(*(pt / self._dpi_ratio for pt in rect))
        else:
            def _draw_rect_callback(painter):
                return
        self._draw_rect_callback = _draw_rect_callback
        self.update()
