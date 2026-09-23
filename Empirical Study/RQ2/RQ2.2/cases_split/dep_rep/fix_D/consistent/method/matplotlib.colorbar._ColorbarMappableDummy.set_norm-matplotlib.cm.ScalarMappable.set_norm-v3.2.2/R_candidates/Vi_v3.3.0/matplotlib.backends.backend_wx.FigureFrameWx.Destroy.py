    def Destroy(self, *args, **kwargs):
        try:
            self.canvas.mpl_disconnect(self.toolbar._id_drag)
            # Rationale for line above: see issue 2941338.
        except AttributeError:
            pass  # classic toolbar lacks the attribute
        # The "if self" check avoids a "wrapped C/C++ object has been deleted"
        # RuntimeError at exit with e.g.
        # MPLBACKEND=wxagg python -c 'from pylab import *; plot()'.
        if self and not self.IsBeingDeleted():
            wx.Frame.Destroy(self, *args, **kwargs)
            if self.toolbar is not None:
                self.toolbar.Destroy()
            wxapp = wx.GetApp()
            if wxapp:
                wxapp.Yield()
        return True
