    def _unstale_viewLim(self):
        # We should arrange to store this information once per share-group
        # instead of on every axis.
        scalex = any(ax._stale_viewlim_x
                     for ax in self._shared_x_axes.get_siblings(self))
        scaley = any(ax._stale_viewlim_y
                     for ax in self._shared_y_axes.get_siblings(self))
        if scalex or scaley:
            for ax in self._shared_x_axes.get_siblings(self):
                ax._stale_viewlim_x = False
            for ax in self._shared_y_axes.get_siblings(self):
                ax._stale_viewlim_y = False
            self.autoscale_view(scalex=scalex, scaley=scaley)
