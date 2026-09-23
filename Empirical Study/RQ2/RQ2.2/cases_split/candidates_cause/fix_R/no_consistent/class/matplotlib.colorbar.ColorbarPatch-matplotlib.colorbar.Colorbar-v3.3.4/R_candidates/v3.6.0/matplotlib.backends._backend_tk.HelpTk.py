@backend_tools._register_tool_class(FigureCanvasTk)
class HelpTk(backend_tools.ToolHelpBase):
    def trigger(self, *args):
        dialog = SimpleDialog(
            self.figure.canvas._tkcanvas, self._get_help_text(), ["OK"])
        dialog.done = lambda num: dialog.frame.master.withdraw()
