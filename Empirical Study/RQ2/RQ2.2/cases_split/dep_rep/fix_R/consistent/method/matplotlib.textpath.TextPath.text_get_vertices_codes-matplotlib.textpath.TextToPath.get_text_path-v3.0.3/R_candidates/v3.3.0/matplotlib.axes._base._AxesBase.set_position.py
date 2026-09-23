    def set_position(self, pos, which='both'):
        """
        Set the axes position.

        Axes have two position attributes. The 'original' position is the
        position allocated for the Axes. The 'active' position is the
        position the Axes is actually drawn at. These positions are usually
        the same unless a fixed aspect is set to the Axes. See `.set_aspect`
        for details.

        Parameters
        ----------
        pos : [left, bottom, width, height] or `~matplotlib.transforms.Bbox`
            The new position of the in `.Figure` coordinates.

        which : {'both', 'active', 'original'}, default: 'both'
            Determines which position variables to change.

        """
        self._set_position(pos, which=which)
        # because this is being called externally to the library we
        # zero the constrained layout parts.
        self._layoutbox = None
        self._poslayoutbox = None
