@backend_tools._register_tool_class(FigureCanvasTk)
class ConfigureSubplotsTk(backend_tools.ConfigureSubplotsBase):
    def trigger(self, *args):
        NavigationToolbar2Tk.configure_subplots(self)
