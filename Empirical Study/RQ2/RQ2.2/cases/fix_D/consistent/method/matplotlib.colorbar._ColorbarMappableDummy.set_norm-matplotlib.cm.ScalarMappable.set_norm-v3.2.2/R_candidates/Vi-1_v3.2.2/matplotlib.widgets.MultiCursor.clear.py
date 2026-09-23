    def clear(self, event):
        """clear the cursor"""
        if self.ignore(event):
            return
        if self.useblit:
            self.background = (
                self.canvas.copy_from_bbox(self.canvas.figure.bbox))
        for line in self.vlines + self.hlines:
            line.set_visible(False)
