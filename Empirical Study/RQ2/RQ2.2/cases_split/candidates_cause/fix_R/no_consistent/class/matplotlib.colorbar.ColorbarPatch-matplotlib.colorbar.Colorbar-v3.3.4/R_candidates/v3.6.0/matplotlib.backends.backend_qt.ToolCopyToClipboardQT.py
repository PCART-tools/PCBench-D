@backend_tools._register_tool_class(FigureCanvasQT)
class ToolCopyToClipboardQT(backend_tools.ToolCopyToClipboardBase):
    def trigger(self, *args, **kwargs):
        pixmap = self.canvas.grab()
        QtWidgets.QApplication.instance().clipboard().setPixmap(pixmap)
