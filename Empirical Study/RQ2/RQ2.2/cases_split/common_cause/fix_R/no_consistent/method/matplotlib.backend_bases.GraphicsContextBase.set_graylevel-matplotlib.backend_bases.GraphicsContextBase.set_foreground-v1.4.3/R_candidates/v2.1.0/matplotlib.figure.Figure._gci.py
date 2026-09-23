    def _gci(self):
        """
        helper for :func:`~matplotlib.pyplot.gci`;
        do not use elsewhere.
        """
        # Look first for an image in the current Axes:
        cax = self._axstack.current_key_axes()[1]
        if cax is None:
            return None
        im = cax._gci()
        if im is not None:
            return im

        # If there is no image in the current Axes, search for
        # one in a previously created Axes.  Whether this makes
        # sense is debatable, but it is the documented behavior.
        for ax in reversed(self.axes):
            im = ax._gci()
            if im is not None:
                return im
        return None
