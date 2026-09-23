    @_api.deprecated("3.5")
    def get_label_width(self, lev, fmt, fsize):
        """Return the width of the label in points."""
        if not isinstance(lev, str):
            lev = self.get_text(lev, fmt)
        fig = self.axes.figure
        width = (text.Text(0, 0, lev, figure=fig,
                           size=fsize, fontproperties=self.labelFontProps)
                 .get_window_extent(mpl.tight_layout.get_renderer(fig)).width)
        width *= 72 / fig.dpi
        return width
