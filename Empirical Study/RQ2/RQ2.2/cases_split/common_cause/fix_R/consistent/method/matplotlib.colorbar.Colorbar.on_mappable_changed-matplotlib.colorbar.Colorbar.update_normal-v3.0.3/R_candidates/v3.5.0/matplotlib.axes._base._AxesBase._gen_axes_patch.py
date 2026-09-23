    def _gen_axes_patch(self):
        """
        Returns
        -------
        Patch
            The patch used to draw the background of the Axes.  It is also used
            as the clipping path for any data elements on the Axes.

            In the standard axes, this is a rectangle, but in other projections
            it may not be.

        Notes
        -----
        Intended to be overridden by new projection types.
        """
        return mpatches.Rectangle((0.0, 0.0), 1.0, 1.0)
