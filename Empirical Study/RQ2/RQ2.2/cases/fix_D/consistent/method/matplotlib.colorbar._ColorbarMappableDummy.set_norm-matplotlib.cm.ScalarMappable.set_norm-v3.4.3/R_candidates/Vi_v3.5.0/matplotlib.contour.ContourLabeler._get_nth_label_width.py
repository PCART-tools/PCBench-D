    def _get_nth_label_width(self, nth):
        """Return the width of the *nth* label, in pixels."""
        fig = self.axes.figure
        return (
            text.Text(0, 0,
                      self.get_text(self.labelLevelList[nth], self.labelFmt),
                      figure=fig,
                      size=self.labelFontSizeList[nth],
                      fontproperties=self.labelFontProps)
            .get_window_extent(mpl.tight_layout.get_renderer(fig)).width)
