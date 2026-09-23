@backend_tools._register_tool_class(_FigureCanvasWxBase)
class ConfigureSubplotsWx(backend_tools.ConfigureSubplotsBase):
    def trigger(self, *args):
        NavigationToolbar2Wx.configure_subplots(self)
