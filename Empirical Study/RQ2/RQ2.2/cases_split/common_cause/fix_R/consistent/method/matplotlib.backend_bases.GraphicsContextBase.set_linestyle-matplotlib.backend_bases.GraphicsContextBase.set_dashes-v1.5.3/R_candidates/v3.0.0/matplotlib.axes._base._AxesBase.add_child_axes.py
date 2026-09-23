    def add_child_axes(self, ax):
        """
        Add a :class:`~matplotlib.axes.Axesbase` instance
        as a child to the axes.

        Returns the added axes.

        This is the lowlevel version.  See `.axes.Axes.inset_axes`
        """

        # normally axes have themselves as the axes, but these need to have
        # their parent...
        # Need to bypass the getter...
        ax._axes = self
        ax.stale_callback = martist._stale_axes_callback

        self.child_axes.append(ax)
        ax._remove_method = self.child_axes.remove
        self.stale = True
        return ax
