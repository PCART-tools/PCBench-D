    def set_location(self, location, transform=None):
        """
        Set the vertical or horizontal location of the axes in
        parent-normalized coordinates.

        Parameters
        ----------
        location : {'top', 'bottom', 'left', 'right'} or float
            The position to put the secondary axis.  Strings can be 'top' or
            'bottom' for orientation='x' and 'right' or 'left' for
            orientation='y'. A float indicates the relative position on the
            parent Axes to put the new Axes, 0.0 being the bottom (or left)
            and 1.0 being the top (or right).

        transform : `.Transform`, optional
            Transform for the location to use. Defaults to
            the parent's ``transAxes``, so locations are normally relative to
            the parent axes.

            .. versionadded:: 3.9
        """

        _api.check_isinstance((transforms.Transform, None), transform=transform)

        # This puts the rectangle into figure-relative coordinates.
        if isinstance(location, str):
            _api.check_in_list(self._locstrings, location=location)
            self._pos = 1. if location in ('top', 'right') else 0.
        elif isinstance(location, numbers.Real):
            self._pos = location
        else:
            raise ValueError(
                f"location must be {self._locstrings[0]!r}, "
                f"{self._locstrings[1]!r}, or a float, not {location!r}")

        self._loc = location

        if self._orientation == 'x':
            # An x-secondary axes is like an inset axes from x = 0 to x = 1 and
            # from y = pos to y = pos + eps, in the parent's transAxes coords.
            bounds = [0, self._pos, 1., 1e-10]

            # If a transformation is provided, use its y component rather than
            # the parent's transAxes. This can be used to place axes in the data
            # coords, for instance.
            if transform is not None:
                transform = transforms.blended_transform_factory(
                    self._parent.transAxes, transform)
        else:  # 'y'
            bounds = [self._pos, 0, 1e-10, 1]
            if transform is not None:
                transform = transforms.blended_transform_factory(
                    transform, self._parent.transAxes)  # Use provided x axis

        # If no transform is provided, use the parent's transAxes
        if transform is None:
            transform = self._parent.transAxes

        # this locator lets the axes move in the parent axes coordinates.
        # so it never needs to know where the parent is explicitly in
        # figure coordinates.
        # it gets called in ax.apply_aspect() (of all places)
        self.set_axes_locator(_TransformedBoundsLocator(bounds, transform))
