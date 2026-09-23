    def __init__(self, canvas, num):
        self._gtk_ver = gtk_ver = Gtk.get_major_version()

        app = _create_application()
        self.window = Gtk.Window()
        app.add_window(self.window)
        super().__init__(canvas, num)

        if gtk_ver == 3:
            self.window.set_wmclass("matplotlib", "Matplotlib")
            icon_ext = "png" if sys.platform == "win32" else "svg"
            self.window.set_icon_from_file(
                str(cbook._get_data_path(f"images/matplotlib.{icon_ext}")))

        self.vbox = Gtk.Box()
        self.vbox.set_property("orientation", Gtk.Orientation.VERTICAL)

        if gtk_ver == 3:
            self.window.add(self.vbox)
            self.vbox.show()
            self.canvas.show()
            self.vbox.pack_start(self.canvas, True, True, 0)
        elif gtk_ver == 4:
            self.window.set_child(self.vbox)
            self.vbox.prepend(self.canvas)

        # calculate size for window
        w, h = self.canvas.get_width_height()

        if self.toolbar is not None:
            if gtk_ver == 3:
                self.toolbar.show()
                self.vbox.pack_end(self.toolbar, False, False, 0)
            elif gtk_ver == 4:
                sw = Gtk.ScrolledWindow(vscrollbar_policy=Gtk.PolicyType.NEVER)
                sw.set_child(self.toolbar)
                self.vbox.append(sw)
            min_size, nat_size = self.toolbar.get_preferred_size()
            h += nat_size.height

        self.window.set_default_size(w, h)

        self._destroying = False
        self.window.connect("destroy", lambda *args: Gcf.destroy(self))
        self.window.connect({3: "delete_event", 4: "close-request"}[gtk_ver],
                            lambda *args: Gcf.destroy(self))
        if mpl.is_interactive():
            self.window.show()
            self.canvas.draw_idle()

        self.canvas.grab_focus()
