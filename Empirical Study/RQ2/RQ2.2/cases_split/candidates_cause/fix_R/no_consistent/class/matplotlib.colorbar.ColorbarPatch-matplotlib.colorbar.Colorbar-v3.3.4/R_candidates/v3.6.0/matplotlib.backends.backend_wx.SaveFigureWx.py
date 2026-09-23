@backend_tools._register_tool_class(_FigureCanvasWxBase)
class SaveFigureWx(backend_tools.SaveFigureBase):
    def trigger(self, *args):
        NavigationToolbar2Wx.save_figure(
            self._make_classic_style_pseudo_toolbar())
