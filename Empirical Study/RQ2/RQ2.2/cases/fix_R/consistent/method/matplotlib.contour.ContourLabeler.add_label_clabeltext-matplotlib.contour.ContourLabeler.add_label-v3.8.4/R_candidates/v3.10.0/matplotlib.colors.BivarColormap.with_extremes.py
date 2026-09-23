    def with_extremes(self, *, bad=None, outside=None, shape=None, origin=None):
        """
        Return a copy of the `BivarColormap` with modified attributes.

        Note that the *outside* color is only relevant if `shape` = 'ignore'
        or 'circleignore'.

        Parameters
        ----------
        bad : None or :mpltype:`color`
            If Matplotlib color, the *bad* value is set accordingly in the copy

        outside : None or :mpltype:`color`
            If Matplotlib color and shape is 'ignore' or 'circleignore', values
            *outside* the colormap are colored accordingly in the copy

        shape : {'square', 'circle', 'ignore', 'circleignore'}

            - If 'square' each variate is clipped to [0,1] independently
            - If 'circle' the variates are clipped radially to the center
              of the colormap, and a circular mask is applied when the colormap
              is displayed
            - If 'ignore' the variates are not clipped, but instead assigned the
              *outside* color
            - If 'circleignore' a circular mask is applied, but the data is not
              clipped and instead assigned the *outside* color

        origin : (float, float)
            The relative origin of the colormap. Typically (0, 0), for colormaps
            that are linear on both axis, and (.5, .5) for circular colormaps.
            Used when getting 1D colormaps from 2D colormaps.

        Returns
        -------
        BivarColormap
            copy of self with attributes set
        """
        new_cm = self.copy()
        if bad is not None:
            new_cm._rgba_bad = to_rgba(bad)
        if outside is not None:
            new_cm._rgba_outside = to_rgba(outside)
        if shape is not None:
            _api.check_in_list(['square', 'circle', 'ignore', 'circleignore'],
                               shape=shape)
            new_cm._shape = shape
        if origin is not None:
            new_cm._origin = (float(origin[0]), float(origin[1]))

        return new_cm
