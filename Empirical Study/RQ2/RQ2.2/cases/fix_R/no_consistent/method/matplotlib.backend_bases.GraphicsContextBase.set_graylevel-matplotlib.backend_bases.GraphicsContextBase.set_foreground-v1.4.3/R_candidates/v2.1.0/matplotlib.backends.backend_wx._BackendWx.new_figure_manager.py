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
        return super(_BackendWx, cls).new_figure_manager(num, *args, **kwargs)
