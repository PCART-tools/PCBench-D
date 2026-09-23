@backend_tools._register_tool_class(_FigureCanvasWxBase)
class RubberbandWx(backend_tools.RubberbandBase):
    def draw_rubberband(self, x0, y0, x1, y1):
        NavigationToolbar2Wx.draw_rubberband(
            self._make_classic_style_pseudo_toolbar(), None, x0, y0, x1, y1)

    def remove_rubberband(self):
        NavigationToolbar2Wx.remove_rubberband(
            self._make_classic_style_pseudo_toolbar())
