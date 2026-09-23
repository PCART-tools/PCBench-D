    def _mouse_move(self, event):
        """Callback for mouse moves in zoom-to-rectangle mode."""

        if self._xypress:
            x, y = event.x, event.y
            lastx, lasty, a, ind, view = self._xypress[0]
            (x1, y1), (x2, y2) = np.clip(
                [[lastx, lasty], [x, y]], a.bbox.min, a.bbox.max)
            if self._zoom_mode == "x":
                y1, y2 = a.bbox.intervaly
            elif self._zoom_mode == "y":
                x1, x2 = a.bbox.intervalx
            self.toolmanager.trigger_tool(
                'rubberband', self, data=(x1, y1, x2, y2))
