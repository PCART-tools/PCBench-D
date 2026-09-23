    def _get_tick1line(self):
        'Get the default line2D instance'
        # x in data coords, y in axes coords
        l = mlines.Line2D(xdata=(0,), ydata=(0,), color=self._color,
                          linestyle='None', marker=self._tickmarkers[0],
                          markersize=self._size,
                          markeredgewidth=self._width, zorder=self._zorder)
        l.set_transform(self.axes.get_xaxis_transform(which='tick1'))
        self._set_artist_props(l)
        return l
