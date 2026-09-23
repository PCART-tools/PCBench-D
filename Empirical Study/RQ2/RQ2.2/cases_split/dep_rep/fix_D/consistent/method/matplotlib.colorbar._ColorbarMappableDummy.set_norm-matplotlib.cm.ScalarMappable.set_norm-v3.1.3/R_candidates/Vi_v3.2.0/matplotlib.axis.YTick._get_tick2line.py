    def _get_tick2line(self):
        'Get the default line2D instance'
        # x in axes coords, y in data coords
        l = mlines.Line2D((1,), (0,),
                          color=self._color,
                          marker=self._tickmarkers[1],
                          linestyle='None',
                          markersize=self._size,
                          markeredgewidth=self._width,
                          zorder=self._zorder)
        l.set_transform(self.axes.get_yaxis_transform(which='tick2'))
        self._set_artist_props(l)
        return l
