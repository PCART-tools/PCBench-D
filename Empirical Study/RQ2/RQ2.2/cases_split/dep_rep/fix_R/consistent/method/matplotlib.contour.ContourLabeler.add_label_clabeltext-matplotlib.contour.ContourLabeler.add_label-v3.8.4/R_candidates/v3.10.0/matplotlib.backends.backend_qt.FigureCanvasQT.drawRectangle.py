    def drawRectangle(self, rect):
        # Draw the zoom rectangle to the QPainter.  _draw_rect_callback needs
        # to be called at the end of paintEvent.
        if rect is not None:
            x0, y0, w, h = (int(pt / self.device_pixel_ratio) for pt in rect)
            x1 = x0 + w
            y1 = y0 + h
            def _draw_rect_callback(painter):
                pen = QtGui.QPen(
                    QtGui.QColor("black"),
                    1 / self.device_pixel_ratio
                )

                pen.setDashPattern([3, 3])
                for color, offset in [
                        (QtGui.QColor("black"), 0),
                        (QtGui.QColor("white"), 3),
                ]:
                    pen.setDashOffset(offset)
                    pen.setColor(color)
                    painter.setPen(pen)
                    # Draw the lines from x0, y0 towards x1, y1 so that the
                    # dashes don't "jump" when moving the zoom box.
                    painter.drawLine(x0, y0, x0, y1)
                    painter.drawLine(x0, y0, x1, y0)
                    painter.drawLine(x0, y1, x1, y1)
                    painter.drawLine(x1, y0, x1, y1)
        else:
            def _draw_rect_callback(painter):
                return
        self._draw_rect_callback = _draw_rect_callback
        self.update()
