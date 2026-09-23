    def clear(self, event):
        """Clear the cursor."""
        if self.ignore(event):
            return
        if self.useblit:
            for canvas, info in self._canvas_infos.items():
                info["background"] = canvas.copy_from_bbox(canvas.figure.bbox)
        for line in self.vlines + self.hlines:
            line.set_visible(False)
