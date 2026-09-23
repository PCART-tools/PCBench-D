    def configure_subplots(self, button):
        toolfig = Figure(figsize=(6, 3))
        canvas = self._get_canvas(toolfig)
        toolfig.subplots_adjust(top=0.9)
        tool = SubplotTool(self.canvas.figure, toolfig)

        w = int(toolfig.bbox.width)
        h = int(toolfig.bbox.height)

        window = Gtk.Window()
        try:
            window.set_icon_from_file(window_icon)
        except Exception:
            # we presumably already logged a message on the
            # failure of the main plot, don't keep reporting
            pass
        window.set_title("Subplot Configuration Tool")
        window.set_default_size(w, h)
        vbox = Gtk.Box()
        vbox.set_property("orientation", Gtk.Orientation.VERTICAL)
        window.add(vbox)
        vbox.show()

        canvas.show()
        vbox.pack_start(canvas, True, True, 0)
        window.show()
