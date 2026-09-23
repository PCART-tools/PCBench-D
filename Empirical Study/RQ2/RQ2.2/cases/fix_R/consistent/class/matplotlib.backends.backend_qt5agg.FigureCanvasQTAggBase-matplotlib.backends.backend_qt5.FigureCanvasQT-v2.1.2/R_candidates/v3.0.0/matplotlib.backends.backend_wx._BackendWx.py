@_Backend.export
class _BackendWx(_Backend):
    required_interactive_framework = "wx"
    FigureCanvas = FigureCanvasWx
    FigureManager = FigureManagerWx
    _frame_class = FigureFrameWx

    @staticmethod
    def trigger_manager_draw(manager):
        manager.canvas.draw_idle()

    @classmethod
    def new_figure_manager(cls, num, *args, **kwargs):
        # Create a wx.App instance if it has not been created sofar.
        wxapp = wx.GetApp()
        if wxapp is None:
            wxapp = wx.App(False)
            wxapp.SetExitOnFrameDelete(True)
            # Retain a reference to the app object so that it does not get
            # garbage collected.
            _BackendWx._theWxApp = wxapp
        return super().new_figure_manager(num, *args, **kwargs)

    @classmethod
    def new_figure_manager_given_figure(cls, num, figure):
        frame = cls._frame_class(num, figure)
        figmgr = frame.get_figure_manager()
        if matplotlib.is_interactive():
            figmgr.frame.Show()
            figure.canvas.draw_idle()
        return figmgr

    @staticmethod
    def mainloop():
        if not wx.App.IsMainLoopRunning():
            wxapp = wx.GetApp()
            if wxapp is not None:
                wxapp.MainLoop()
