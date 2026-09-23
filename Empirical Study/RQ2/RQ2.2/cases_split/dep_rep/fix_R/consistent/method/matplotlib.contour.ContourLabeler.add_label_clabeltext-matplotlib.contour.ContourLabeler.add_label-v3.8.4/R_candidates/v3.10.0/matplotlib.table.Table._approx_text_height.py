    def _approx_text_height(self):
        return (self.FONTSIZE / 72.0 * self.get_figure(root=True).dpi /
                self._axes.bbox.height * 1.2)
