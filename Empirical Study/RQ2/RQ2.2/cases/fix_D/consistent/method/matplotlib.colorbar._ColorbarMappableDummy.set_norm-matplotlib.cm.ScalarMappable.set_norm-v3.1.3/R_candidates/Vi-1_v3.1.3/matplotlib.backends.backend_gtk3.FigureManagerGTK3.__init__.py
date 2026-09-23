    def __init__(self, canvas, num):
        FigureManagerBase.__init__(self, canvas, num)

        self.window = Gtk.Window()
        self.window.set_wmclass("matplotlib", "Matplotlib")
        self.set_window_title("Figure %d" % num)
        try:
            self.window.set_icon_from_file(window_icon)
        except Exception:
            # Some versions of gtk throw a glib.GError but not all, so I am not
            # sure how to catch it.  I am unhappy doing a blanket catch here,
            # but am not sure what a better way is - JDH
            _log.info('Could not load matplotlib icon: %s', sys.exc_info()[1])

        self.vbox = Gtk.Box()
        self.vbox.set_property("orientation", Gtk.Orientation.VERTICAL)
        self.window.add(self.vbox)
        self.vbox.show()

        self.canvas.show()

        self.vbox.pack_start(self.canvas, True, True, 0)
        # calculate size for window
        w = int(self.canvas.figure.bbox.width)
        h = int(self.canvas.figure.bbox.height)

        self.toolmanager = self._get_toolmanager()
        self.toolbar = self._get_toolbar()
        self.statusbar = None

        def add_widget(child, expand, fill, padding):
            child.show()
            self.vbox.pack_end(child, False, False, 0)
            size_request = child.size_request()
            return size_request.height

        if self.toolmanager:
            backend_tools.add_tools_to_manager(self.toolmanager)
            if self.toolbar:
                backend_tools.add_tools_to_container(self.toolbar)
                self.statusbar = StatusbarGTK3(self.toolmanager)
                h += add_widget(self.statusbar, False, False, 0)
                h += add_widget(Gtk.HSeparator(), False, False, 0)

        if self.toolbar is not None:
            self.toolbar.show()
            h += add_widget(self.toolbar, False, False, 0)

        self.window.set_default_size(w, h)

        def destroy(*args):
            Gcf.destroy(num)
        self.window.connect("destroy", destroy)
        self.window.connect("delete_event", destroy)
        if matplotlib.is_interactive():
            self.window.show()
            self.canvas.draw_idle()

        self.canvas.grab_focus()
