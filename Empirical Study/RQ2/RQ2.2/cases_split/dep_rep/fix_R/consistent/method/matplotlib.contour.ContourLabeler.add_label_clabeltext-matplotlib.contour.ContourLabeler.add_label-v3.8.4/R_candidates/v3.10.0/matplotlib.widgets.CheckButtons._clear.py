    def _clear(self, event):
        """Internal event handler to clear the buttons."""
        if self.ignore(event) or self.canvas.is_saving():
            return
        self._background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self._checks)
