    @staticmethod
    def mainloop():
        if not wx.App.IsMainLoopRunning():
            wxapp = wx.GetApp()
            if wxapp is not None:
                wxapp.MainLoop()
