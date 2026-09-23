    def destroy(self, *args):
        DEBUG_MSG("destroy()", 1, self)
        self.frame.Destroy()
        wxapp = wx.GetApp()
        if wxapp:
            wxapp.Yield()
