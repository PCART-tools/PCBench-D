    def _clear(self, event):
        """Internal event handler to clear the buttons."""
        if self.ignore(event) or self._changed_canvas():
            return
        self._background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self._buttons)
        if hasattr(self, "_circles"):
            for circle in self._circles:
                self.ax.draw_artist(circle)
