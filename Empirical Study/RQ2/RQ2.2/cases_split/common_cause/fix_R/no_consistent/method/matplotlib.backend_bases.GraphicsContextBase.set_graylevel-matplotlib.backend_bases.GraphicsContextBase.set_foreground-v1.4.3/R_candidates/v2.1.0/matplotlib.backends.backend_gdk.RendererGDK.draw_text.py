    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        x, y = int(x), int(y)

        if x < 0 or y < 0: # window has shrunk and text is off the edge
            return

        if angle not in (0,90):
            warnings.warn('backend_gdk: unable to draw text at angles ' +
                          'other than 0 or 90')
        elif ismath:
            self._draw_mathtext(gc, x, y, s, prop, angle)

        elif angle==90:
            self._draw_rotated_text(gc, x, y, s, prop, angle)

        else:
            layout, inkRect, logicalRect = self._get_pango_layout(s, prop)
            l, b, w, h = inkRect
            if (x + w > self.width or y + h > self.height):
                return

            self.gdkDrawable.draw_layout(gc.gdkGC, x, y-h-b, layout)
