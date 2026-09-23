    def destroy(self, *args):
        # docstring inherited
        _log.debug("%s - destroy()", type(self))
        frame = self.frame
        if frame:  # Else, may have been already deleted, e.g. when closing.
            # As this can be called from non-GUI thread from plt.close use
            # wx.CallAfter to ensure thread safety.
            wx.CallAfter(frame.Close)
