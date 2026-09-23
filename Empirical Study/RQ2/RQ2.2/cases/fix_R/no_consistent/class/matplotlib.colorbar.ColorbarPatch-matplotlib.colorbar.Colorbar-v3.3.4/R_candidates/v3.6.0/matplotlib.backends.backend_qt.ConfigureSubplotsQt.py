@backend_tools._register_tool_class(FigureCanvasQT)
class ConfigureSubplotsQt(backend_tools.ConfigureSubplotsBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._subplot_dialog = None

    def trigger(self, *args):
        NavigationToolbar2QT.configure_subplots(self)
