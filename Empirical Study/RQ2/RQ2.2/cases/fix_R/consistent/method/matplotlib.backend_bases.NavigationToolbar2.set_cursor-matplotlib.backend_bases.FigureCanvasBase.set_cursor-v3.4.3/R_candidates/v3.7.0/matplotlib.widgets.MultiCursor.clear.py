    def clear(self, event):
        """Clear the cursor."""
        if self.ignore(event):
            return
        if self.useblit:
            for canvas, info in self._canvas_infos.items():
                # someone has switched the canvas on us!  This happens if
                # `savefig` needs to save to a format the previous backend did
                # not support (e.g. saving a figure using an Agg based backend
                # saved to a vector format).
                if canvas is not canvas.figure.canvas:
                    continue
                info["background"] = canvas.copy_from_bbox(canvas.figure.bbox)
