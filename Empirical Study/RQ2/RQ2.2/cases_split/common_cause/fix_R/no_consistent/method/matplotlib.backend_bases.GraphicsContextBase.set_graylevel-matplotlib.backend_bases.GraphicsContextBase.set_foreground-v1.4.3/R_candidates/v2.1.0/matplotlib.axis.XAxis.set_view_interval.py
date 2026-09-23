    def set_view_interval(self, vmin, vmax, ignore=False):
        """
        If *ignore* is *False*, the order of vmin, vmax
        does not matter; the original axis orientation will
        be preserved. In addition, the view limits can be
        expanded, but will not be reduced.  This method is
        for mpl internal use; for normal use, see
        :meth:`~matplotlib.axes.Axes.set_xlim`.

        """
        if ignore:
            self.axes.viewLim.intervalx = vmin, vmax
        else:
            Vmin, Vmax = self.get_view_interval()
            if Vmin < Vmax:
                self.axes.viewLim.intervalx = (min(vmin, vmax, Vmin),
                                               max(vmin, vmax, Vmax))
            else:
                self.axes.viewLim.intervalx = (max(vmin, vmax, Vmin),
                                               min(vmin, vmax, Vmax))
