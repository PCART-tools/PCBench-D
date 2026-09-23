class ConfigureSubplotsGTK3(backend_tools.ConfigureSubplotsBase, Gtk.Window):
    def __init__(self, *args, **kwargs):
        backend_tools.ConfigureSubplotsBase.__init__(self, *args, **kwargs)
        self.window = None

    def init_window(self):
        if self.window:
            return
        self.window = Gtk.Window(title="Subplot Configuration Tool")

        try:
            self.window.window.set_icon_from_file(window_icon)
        except Exception:
            # we presumably already logged a message on the
            # failure of the main plot, don't keep reporting
            pass

        self.vbox = Gtk.Box()
        self.vbox.set_property("orientation", Gtk.Orientation.VERTICAL)
        self.window.add(self.vbox)
        self.vbox.show()
        self.window.connect('destroy', self.destroy)

        toolfig = Figure(figsize=(6, 3))
        canvas = self.figure.canvas.__class__(toolfig)

        toolfig.subplots_adjust(top=0.9)
        SubplotTool(self.figure, toolfig)

        w = int(toolfig.bbox.width)
        h = int(toolfig.bbox.height)

        self.window.set_default_size(w, h)

        canvas.show()
        self.vbox.pack_start(canvas, True, True, 0)
        self.window.show()

    def destroy(self, *args):
        self.window.destroy()
        self.window = None

    def _get_canvas(self, fig):
        return self.canvas.__class__(fig)

    def trigger(self, sender, event, data=None):
        self.init_window()
        self.window.present()
