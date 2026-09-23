    def _get_gridline(self):
        'Get the default line2D instance'
        # x in axes coords, y in data coords
        l = mlines.Line2D(xdata=(0, 1), ydata=(0, 0),
                          color=self._grid_color,
                          linestyle=self._grid_linestyle,
                          linewidth=self._grid_linewidth,
                          alpha=self._grid_alpha,
                          markersize=0,
                          **self._grid_kw)
        l.set_transform(self.axes.get_yaxis_transform(which='grid'))
        l.get_path()._interpolation_steps = GRIDLINE_INTERPOLATION_STEPS
        self._set_artist_props(l)
        return l
