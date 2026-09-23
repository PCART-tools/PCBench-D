    def update_from(self, other):
        """
        Updates this :class:`Patch` from the properties of *other*.
        """
        artist.Artist.update_from(self, other)
        # For some properties we don't need or don't want to go through the
        # getters/setters, so we just copy them directly.
        self._edgecolor = other._edgecolor
        self._facecolor = other._facecolor
        self._fill = other._fill
        self._hatch = other._hatch
        self._hatch_color = other._hatch_color
        # copy the unscaled dash pattern
        self._us_dashes = other._us_dashes
        self.set_linewidth(other._linewidth)  # also sets dash properties
        self.set_transform(other.get_data_transform())
