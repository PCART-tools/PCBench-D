    def _get_gridline(self):
        'Get the default line2D instance'
        # x in axes coords, y in data coords
        l = mlines.Line2D(xdata=(0, 1), ydata=(0, 0),
                          color=rcParams['grid.color'],
                          linestyle=rcParams['grid.linestyle'],
                          linewidth=rcParams['grid.linewidth'],
                          alpha=rcParams['grid.alpha'],
                          markersize=0)

        l.set_transform(self.axes.get_yaxis_transform(which='grid'))
        l.get_path()._interpolation_steps = GRIDLINE_INTERPOLATION_STEPS
        self._set_artist_props(l)
        return l
