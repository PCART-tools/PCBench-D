    def update_from(self, other):
        'copy properties from other to self'

        artist.Artist.update_from(self, other)
        self._antialiaseds = other._antialiaseds
        self._original_edgecolor = other._original_edgecolor
        self._edgecolors = other._edgecolors
        self._original_facecolor = other._original_facecolor
        self._facecolors = other._facecolors
        self._linewidths = other._linewidths
        self._linestyles = other._linestyles
        self._us_linestyles = other._us_linestyles
        self._pickradius = other._pickradius
        self._hatch = other._hatch

        # update_from for scalarmappable
        self._A = other._A
        self.norm = other.norm
        self.cmap = other.cmap
        # self.update_dict = other.update_dict # do we need to copy this? -JJL
        self.stale = True
