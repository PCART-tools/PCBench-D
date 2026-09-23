    def delaxes(self, ax):
        """
        Remove the `~.axes.Axes` *ax* from the figure; update the current Axes.
        """
        self._remove_axes(ax, owners=[self._axstack, self._localaxes])
