@backend_tools._register_tool_class(_FigureCanvasWxBase)
class HelpWx(backend_tools.ToolHelpBase):
    def trigger(self, *args):
        _HelpDialog.show(self.figure.canvas.GetTopLevelParent(),
                         self._get_help_entries())
