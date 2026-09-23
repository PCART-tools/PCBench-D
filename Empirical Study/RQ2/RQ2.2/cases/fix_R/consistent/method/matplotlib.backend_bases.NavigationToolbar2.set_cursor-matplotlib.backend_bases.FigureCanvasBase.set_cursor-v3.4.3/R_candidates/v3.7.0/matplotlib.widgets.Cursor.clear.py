    def clear(self, event):
        """Internal event handler to clear the cursor."""
        if self.ignore(event) or self._changed_canvas():
            return
        if self.useblit:
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
