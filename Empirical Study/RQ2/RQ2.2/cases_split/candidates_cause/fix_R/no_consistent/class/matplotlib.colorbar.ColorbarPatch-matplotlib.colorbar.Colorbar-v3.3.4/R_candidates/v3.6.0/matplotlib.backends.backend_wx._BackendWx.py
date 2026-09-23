@_Backend.export
class _BackendWx(_Backend):
    FigureCanvas = FigureCanvasWx
    FigureManager = FigureManagerWx

    @staticmethod
    def mainloop():
        if not wx.App.IsMainLoopRunning():
            wxapp = wx.GetApp()
            if wxapp is not None:
                wxapp.MainLoop()
