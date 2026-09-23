    @cbook.deprecated("3.2")
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
