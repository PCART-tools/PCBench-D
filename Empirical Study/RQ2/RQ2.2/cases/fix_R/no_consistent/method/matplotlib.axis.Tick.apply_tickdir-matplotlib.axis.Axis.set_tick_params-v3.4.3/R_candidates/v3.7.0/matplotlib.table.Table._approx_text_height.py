    def _approx_text_height(self):
        return (self.FONTSIZE / 72.0 * self.figure.dpi /
                self._axes.bbox.height * 1.2)
