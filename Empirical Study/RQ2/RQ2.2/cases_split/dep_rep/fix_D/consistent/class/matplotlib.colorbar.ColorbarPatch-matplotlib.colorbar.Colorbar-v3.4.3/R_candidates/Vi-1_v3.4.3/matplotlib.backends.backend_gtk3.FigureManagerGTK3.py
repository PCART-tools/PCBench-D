class FigureManagerGTK3(FigureManagerBase):
    """
    Attributes
    ----------
    canvas : `FigureCanvas`
        The FigureCanvas instance
    num : int or str
        The Figure number
    toolbar : Gtk.Toolbar
        The Gtk.Toolbar
    vbox : Gtk.VBox
        The Gtk.VBox containing the canvas and toolbar
    window : Gtk.Window
        The Gtk.Window

    """
    def __init__(self, canvas, num):
        self.window = Gtk.Window()
        super().__init__(canvas, num)

        self.window.set_wmclass("matplotlib", "Matplotlib")
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

        self.toolbar = self._get_toolbar()

        if self.toolmanager:
            backend_tools.add_tools_to_manager(self.toolmanager)
            if self.toolbar:
                backend_tools.add_tools_to_container(self.toolbar)

        if self.toolbar is not None:
            self.toolbar.show()
            self.vbox.pack_end(self.toolbar, False, False, 0)
            min_size, nat_size = self.toolbar.get_preferred_size()
            h += nat_size.height

        self.window.set_default_size(w, h)

        self._destroying = False
        self.window.connect("destroy", lambda *args: Gcf.destroy(self))
        self.window.connect("delete_event", lambda *args: Gcf.destroy(self))
        if mpl.is_interactive():
            self.window.show()
            self.canvas.draw_idle()

        self.canvas.grab_focus()

    def destroy(self, *args):
        if self._destroying:
            # Otherwise, this can be called twice when the user presses 'q',
            # which calls Gcf.destroy(self), then this destroy(), then triggers
            # Gcf.destroy(self) once again via
            # `connect("destroy", lambda *args: Gcf.destroy(self))`.
            return
        self._destroying = True
        self.vbox.destroy()
        self.window.destroy()
        self.canvas.destroy()
        if self.toolbar:
            self.toolbar.destroy()

        if (Gcf.get_num_fig_managers() == 0 and not mpl.is_interactive() and
                Gtk.main_level() >= 1):
            Gtk.main_quit()

    def show(self):
        # show the figure window
        self.window.show()
        self.canvas.draw()
        if mpl.rcParams['figure.raise_window']:
            if self.window.get_window():
                self.window.present()
            else:
                # If this is called by a callback early during init,
                # self.window (a GtkWindow) may not have an associated
                # low-level GdkWindow (self.window.get_window()) yet, and
                # present() would crash.
                _api.warn_external("Cannot raise window yet to be setup")

    def full_screen_toggle(self):
        self._full_screen_flag = not self._full_screen_flag
        if self._full_screen_flag:
            self.window.fullscreen()
        else:
            self.window.unfullscreen()
    _full_screen_flag = False

    def _get_toolbar(self):
        # must be inited after the window, drawingArea and figure
        # attrs are set
        if mpl.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2GTK3(self.canvas, self.window)
        elif mpl.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarGTK3(self.toolmanager)
        else:
            toolbar = None
        return toolbar

    def get_window_title(self):
        return self.window.get_title()

    def set_window_title(self, title):
        self.window.set_title(title)

    def resize(self, width, height):
        """Set the canvas size in pixels."""
        if self.toolbar:
            toolbar_size = self.toolbar.size_request()
            height += toolbar_size.height
        canvas_size = self.canvas.get_allocation()
        if canvas_size.width == canvas_size.height == 1:
            # A canvas size of (1, 1) cannot exist in most cases, because
            # window decorations would prevent such a small window. This call
            # must be before the window has been mapped and widgets have been
            # sized, so just change the window's starting size.
            self.window.set_default_size(width, height)
        else:
            self.window.resize(width, height)
