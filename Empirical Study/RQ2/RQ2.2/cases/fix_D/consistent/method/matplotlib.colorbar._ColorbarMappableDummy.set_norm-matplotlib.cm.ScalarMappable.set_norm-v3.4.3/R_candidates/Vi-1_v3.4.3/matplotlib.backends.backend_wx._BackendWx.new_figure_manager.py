    @classmethod
    def new_figure_manager(cls, num, *args, **kwargs):
        # Create a wx.App instance if it has not been created so far.
        wxapp = wx.GetApp()
        if wxapp is None:
            wxapp = wx.App(False)
            wxapp.SetExitOnFrameDelete(True)
            cbook._setup_new_guiapp()
            # Retain a reference to the app object so that it does not get
            # garbage collected.
            _BackendWx._theWxApp = wxapp
        return super().new_figure_manager(num, *args, **kwargs)
