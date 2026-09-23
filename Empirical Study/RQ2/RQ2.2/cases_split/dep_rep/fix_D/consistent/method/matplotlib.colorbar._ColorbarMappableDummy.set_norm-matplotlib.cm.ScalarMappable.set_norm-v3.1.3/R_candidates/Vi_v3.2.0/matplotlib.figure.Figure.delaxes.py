    def delaxes(self, ax):
        """
        Remove the `~matplotlib.axes.Axes` *ax* from the figure and update the
        current axes.
        """
        self._axstack.remove(ax)
        for func in self._axobservers:
            func(self)
        self.stale = True
