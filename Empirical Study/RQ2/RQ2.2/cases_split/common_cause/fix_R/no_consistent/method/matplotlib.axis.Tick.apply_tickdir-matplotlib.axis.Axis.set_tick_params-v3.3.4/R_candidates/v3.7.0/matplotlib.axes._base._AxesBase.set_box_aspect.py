    def set_box_aspect(self, aspect=None):
        """
        Set the Axes box aspect, i.e. the ratio of height to width.

        This defines the aspect of the Axes in figure space and is not to be
        confused with the data aspect (see `~.Axes.set_aspect`).

        Parameters
        ----------
        aspect : float or None
            Changes the physical dimensions of the Axes, such that the ratio
            of the Axes height to the Axes width in physical units is equal to
            *aspect*. Defining a box aspect will change the *adjustable*
            property to 'datalim' (see `~.Axes.set_adjustable`).

            *None* will disable a fixed box aspect so that height and width
            of the Axes are chosen independently.

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
