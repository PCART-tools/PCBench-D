    def _request_autoscale_view(self, tight=None, scalex=True, scaley=True):
        if tight is not None:
            self._tight = tight
        if scalex:
            self._stale_viewlim_x = True  # Else keep old state.
        if scaley:
            self._stale_viewlim_y = True
