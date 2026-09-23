    def __init__(self, bounds=None, inset_ax=None, zorder=None, **kwargs):
        """
        Parameters
        ----------
        bounds : [x0, y0, width, height], optional
            Lower-left corner of rectangle to be marked, and its width
            and height.  If not set, the bounds will be calculated from the
            data limits of inset_ax, which must be supplied.

        inset_ax : `~.axes.Axes`, optional
            An optional inset Axes to draw connecting lines to.  Two lines are
            drawn connecting the indicator box to the inset Axes on corners
            chosen so as to not overlap with the indicator box.

        zorder : float, default: 4.99
            Drawing order of the rectangle and connector lines.  The default,
            4.99, is just below the default level of inset Axes.

        **kwargs
            Other keyword arguments are passed on to the `.Rectangle` patch.
        """
        if bounds is None and inset_ax is None:
            raise ValueError("At least one of bounds or inset_ax must be supplied")

        self._inset_ax = inset_ax

        if bounds is None:
            # Work out bounds from inset_ax
            self._auto_update_bounds = True
            bounds = self._bounds_from_inset_ax()
        else:
            self._auto_update_bounds = False

        x, y, width, height = bounds

        self._rectangle = Rectangle((x, y), width, height, clip_on=False, **kwargs)

        # Connector positions cannot be calculated till the artist has been added
        # to an axes, so just make an empty list for now.
        self._connectors = []

        super().__init__()
        self.set_zorder(zorder)

        # Initial style properties for the artist should match the rectangle.
        for prop in _shared_properties:
            setattr(self, f'_{prop}', artist.getp(self._rectangle, prop))
