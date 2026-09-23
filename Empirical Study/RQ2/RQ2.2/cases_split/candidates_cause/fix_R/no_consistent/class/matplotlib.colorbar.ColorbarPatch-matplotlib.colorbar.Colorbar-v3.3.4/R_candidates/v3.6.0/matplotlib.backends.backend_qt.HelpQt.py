@backend_tools._register_tool_class(FigureCanvasQT)
class HelpQt(backend_tools.ToolHelpBase):
    def trigger(self, *args):
        QtWidgets.QMessageBox.information(None, "Help", self._get_help_html())
