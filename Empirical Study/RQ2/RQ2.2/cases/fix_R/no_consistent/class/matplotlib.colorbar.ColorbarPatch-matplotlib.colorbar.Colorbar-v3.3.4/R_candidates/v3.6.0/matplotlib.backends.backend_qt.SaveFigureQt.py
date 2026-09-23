@backend_tools._register_tool_class(FigureCanvasQT)
class SaveFigureQt(backend_tools.SaveFigureBase):
    def trigger(self, *args):
        NavigationToolbar2QT.save_figure(
            self._make_classic_style_pseudo_toolbar())
