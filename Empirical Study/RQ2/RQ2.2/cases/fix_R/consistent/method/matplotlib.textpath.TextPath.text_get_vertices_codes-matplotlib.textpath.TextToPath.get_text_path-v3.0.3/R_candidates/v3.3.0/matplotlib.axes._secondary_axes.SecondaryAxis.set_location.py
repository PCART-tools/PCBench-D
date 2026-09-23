    def set_location(self, location):
        """
        Set the vertical or horizontal location of the axes in
        parent-normalized coordinates.

        Parameters
        ----------
        location : {'top', 'bottom', 'left', 'right'} or float
            The position to put the secondary axis.  Strings can be 'top' or
            'bottom' for orientation='x' and 'right' or 'left' for
            orientation='y'. A float indicates the relative position on the
            parent axes to put the new axes, 0.0 being the bottom (or left)
            and 1.0 being the top (or right).
        """

        # This puts the rectangle into figure-relative coordinates.
        if isinstance(location, str):
            if location in ['top', 'right']:
                self._pos = 1.
            elif location in ['bottom', 'left']:
                self._pos = 0.
            else:
                raise ValueError(
                    f"location must be {self._locstrings[0]!r}, "
                    f"{self._locstrings[1]!r}, or a float, not {location!r}")
        else:
            self._pos = location
        self._loc = location

        if self._orientation == 'x':
            bounds = [0, self._pos, 1., 1e-10]
        else:
            bounds = [self._pos, 0, 1e-10, 1]

        secondary_locator = _make_secondary_locator(bounds, self._parent)

        # this locator lets the axes move in the parent axes coordinates.
        # so it never needs to know where the parent is explicitly in
        # figure coordinates.
        # it gets called in `ax.apply_aspect() (of all places)
        self.set_axes_locator(secondary_locator)
