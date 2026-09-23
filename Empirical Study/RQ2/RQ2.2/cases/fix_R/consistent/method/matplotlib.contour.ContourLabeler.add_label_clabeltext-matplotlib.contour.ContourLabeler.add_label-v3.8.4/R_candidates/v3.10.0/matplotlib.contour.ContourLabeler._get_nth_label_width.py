    def _get_nth_label_width(self, nth):
        """Return the width of the *nth* label, in pixels."""
        fig = self.axes.get_figure(root=False)
        renderer = fig.get_figure(root=True)._get_renderer()
        return (Text(0, 0,
                     self.get_text(self.labelLevelList[nth], self.labelFmt),
                     figure=fig, fontproperties=self._label_font_props)
                .get_window_extent(renderer).width)
