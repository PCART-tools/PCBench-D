    def _axes_pos(self, ax):
        """
        Return the original and modified positions for the specified axes.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The `.Axes` to get the positions for.

        Returns
        -------
        original_position, modified_position
            A tuple of the original and modified positions.
        """

        return (ax.get_position(True).frozen(),
                ax.get_position().frozen())
