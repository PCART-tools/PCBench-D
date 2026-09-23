    def set_extent(self, extent):
        """
        extent is data axes (left, right, bottom, top) for making image plots

        This updates ax.dataLim, and, if autoscaling, sets viewLim
        to tightly fit the image, regardless of dataLim.  Autoscaling
        state is not changed, so following this with ax.autoscale_view
        will redo the autoscaling in accord with dataLim.
        """
        self._extent = xmin, xmax, ymin, ymax = extent
        corners = (xmin, ymin), (xmax, ymax)
        self.axes.update_datalim(corners)
        self.sticky_edges.x[:] = [xmin, xmax]
        self.sticky_edges.y[:] = [ymin, ymax]
        if self.axes._autoscaleXon:
            self.axes.set_xlim((xmin, xmax), auto=None)
        if self.axes._autoscaleYon:
            self.axes.set_ylim((ymin, ymax), auto=None)
        self.stale = True
