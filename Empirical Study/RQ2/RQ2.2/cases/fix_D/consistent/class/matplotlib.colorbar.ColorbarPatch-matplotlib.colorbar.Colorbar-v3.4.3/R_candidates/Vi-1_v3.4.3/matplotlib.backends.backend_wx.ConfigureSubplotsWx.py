class ConfigureSubplotsWx(backend_tools.ConfigureSubplotsBase):
    def trigger(self, *args):
        NavigationToolbar2Wx.configure_subplots(
            self._make_classic_style_pseudo_toolbar())
