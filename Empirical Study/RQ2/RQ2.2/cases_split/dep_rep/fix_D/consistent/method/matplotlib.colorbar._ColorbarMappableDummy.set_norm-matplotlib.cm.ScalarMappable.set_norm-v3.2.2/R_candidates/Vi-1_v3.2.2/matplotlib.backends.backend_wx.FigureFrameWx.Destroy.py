    def Destroy(self, *args, **kwargs):
        try:
            self.canvas.mpl_disconnect(self.toolbar._idDrag)
            # Rationale for line above: see issue 2941338.
        except AttributeError:
            pass  # classic toolbar lacks the attribute
        if not self.IsBeingDeleted():
            wx.Frame.Destroy(self, *args, **kwargs)
            if self.toolbar is not None:
                self.toolbar.Destroy()
            wxapp = wx.GetApp()
            if wxapp:
                wxapp.Yield()
        return True
