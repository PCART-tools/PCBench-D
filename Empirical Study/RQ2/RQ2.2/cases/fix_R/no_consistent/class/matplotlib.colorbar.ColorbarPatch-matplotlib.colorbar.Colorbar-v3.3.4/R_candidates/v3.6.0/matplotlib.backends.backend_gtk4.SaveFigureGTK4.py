@backend_tools._register_tool_class(FigureCanvasGTK4)
class SaveFigureGTK4(backend_tools.SaveFigureBase):
    def trigger(self, *args, **kwargs):
        NavigationToolbar2GTK4.save_figure(
            self._make_classic_style_pseudo_toolbar())
