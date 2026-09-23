@backend_tools._register_tool_class(FigureCanvasTk)
class RubberbandTk(backend_tools.RubberbandBase):
    def draw_rubberband(self, x0, y0, x1, y1):
        NavigationToolbar2Tk.draw_rubberband(
            self._make_classic_style_pseudo_toolbar(), None, x0, y0, x1, y1)

    def remove_rubberband(self):
        NavigationToolbar2Tk.remove_rubberband(
            self._make_classic_style_pseudo_toolbar())

    lastrect = _api.deprecated("3.6")(
        property(lambda self: self.figure.canvas._rubberband_rect))
