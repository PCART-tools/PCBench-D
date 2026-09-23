    def __init__(self, canvas, num):
        app = _create_application()
        self.window = Gtk.Window()
        app.add_window(self.window)
        super().__init__(canvas, num)

        self.vbox = Gtk.Box()
        self.vbox.set_property("orientation", Gtk.Orientation.VERTICAL)
        self.window.set_child(self.vbox)

        self.vbox.prepend(self.canvas)
        # calculate size for window
        w, h = self.canvas.get_width_height()

        self.toolbar = self._get_toolbar()

        if self.toolmanager:
            backend_tools.add_tools_to_manager(self.toolmanager)
            if self.toolbar:
                backend_tools.add_tools_to_container(self.toolbar)

        if self.toolbar is not None:
            sw = Gtk.ScrolledWindow(vscrollbar_policy=Gtk.PolicyType.NEVER)
            sw.set_child(self.toolbar)
            self.vbox.append(sw)
            min_size, nat_size = self.toolbar.get_preferred_size()
            h += nat_size.height

        self.window.set_default_size(w, h)

        self._destroying = False
        self.window.connect("destroy", lambda *args: Gcf.destroy(self))
        self.window.connect("close-request", lambda *args: Gcf.destroy(self))
        if mpl.is_interactive():
            self.window.show()
            self.canvas.draw_idle()

        self.canvas.grab_focus()
