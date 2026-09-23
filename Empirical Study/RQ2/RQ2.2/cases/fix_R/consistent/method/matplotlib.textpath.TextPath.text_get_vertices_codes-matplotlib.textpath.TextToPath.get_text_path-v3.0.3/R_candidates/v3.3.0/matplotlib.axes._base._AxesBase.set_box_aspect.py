    def set_box_aspect(self, aspect=None):
        """
        Set the axes box aspect. The box aspect is the ratio of the
        axes height to the axes width in physical units. This is not to be
        confused with the data aspect, set via `~.Axes.set_aspect`.

        Parameters
        ----------
        aspect : None, or a number
            Changes the physical dimensions of the Axes, such that the ratio
            of the axes height to the axes width in physical units is equal to
            *aspect*. If *None*, the axes geometry will not be adjusted.

        Note that calling this function with a number changes the *adjustable*
        to *datalim*.

        See Also
        --------
        matplotlib.axes.Axes.set_aspect
            for a description of aspect handling.
        """
        axs = {*self._twinned_axes.get_siblings(self),
               *self._twinned_axes.get_siblings(self)}

        if aspect is not None:
            aspect = float(aspect)
            # when box_aspect is set to other than ´None`,
            # adjustable must be "datalim"
            for ax in axs:
                ax.set_adjustable("datalim")

        for ax in axs:
            ax._box_aspect = aspect
            ax.stale = True
