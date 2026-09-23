    def _clear(self, event):
        """Internal event handler to clear the buttons."""
        if self.ignore(event) or self._changed_canvas():
            return
        self._background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self._checks)
        if hasattr(self, '_lines'):
            for l1, l2 in self._lines:
                self.ax.draw_artist(l1)
                self.ax.draw_artist(l2)
