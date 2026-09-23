    def destroy(self, *args):
        # docstring inherited
        _log.debug("%s - destroy()", type(self))
        frame = self.frame
        if frame:  # Else, may have been already deleted, e.g. when closing.
            frame.Close()
        wxapp = wx.GetApp()
        if wxapp:
            wxapp.Yield()
