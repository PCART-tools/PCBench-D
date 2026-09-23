@backend_tools._register_tool_class(FigureCanvasGTK3)
class ToolCopyToClipboardGTK3(backend_tools.ToolCopyToClipboardBase):
    def trigger(self, *args, **kwargs):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        window = self.canvas.get_window()
        x, y, width, height = window.get_geometry()
        pb = Gdk.pixbuf_get_from_window(window, x, y, width, height)
        clipboard.set_image(pb)
