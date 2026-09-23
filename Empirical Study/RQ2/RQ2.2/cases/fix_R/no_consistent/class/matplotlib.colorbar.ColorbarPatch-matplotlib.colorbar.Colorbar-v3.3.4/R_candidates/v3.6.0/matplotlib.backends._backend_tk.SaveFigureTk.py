@backend_tools._register_tool_class(FigureCanvasTk)
class SaveFigureTk(backend_tools.SaveFigureBase):
    def trigger(self, *args):
        NavigationToolbar2Tk.save_figure(
            self._make_classic_style_pseudo_toolbar())
