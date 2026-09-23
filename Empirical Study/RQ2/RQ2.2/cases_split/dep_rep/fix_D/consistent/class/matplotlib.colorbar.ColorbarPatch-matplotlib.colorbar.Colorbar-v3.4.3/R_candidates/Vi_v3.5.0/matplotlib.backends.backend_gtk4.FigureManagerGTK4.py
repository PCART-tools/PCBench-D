class FigureManagerGTK4(FigureManagerBase):
    """
    Attributes
    ----------
    canvas : `FigureCanvas`
        The FigureCanvas instance
    num : int or str
        The Figure number
    toolbar : Gtk.Box
        The toolbar
    vbox : Gtk.VBox
        The Gtk.VBox containing the canvas and toolbar
    window : Gtk.Window
        The Gtk.Window

    """
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

    def destroy(self, *args):
        if self._destroying:
            # Otherwise, this can be called twice when the user presses 'q',
            # which calls Gcf.destroy(self), then this destroy(), then triggers
            # Gcf.destroy(self) once again via
            # `connect("destroy", lambda *args: Gcf.destroy(self))`.
            return
        self._destroying = True
        self.window.destroy()
        self.canvas.destroy()

    def show(self):
        # show the figure window
        self.window.show()
        self.canvas.draw()
        if mpl.rcParams['figure.raise_window']:
            if self.window.get_surface():
                self.window.present()
            else:
                # If this is called by a callback early during init,
                # self.window (a GtkWindow) may not have an associated
                # low-level GdkSurface (self.window.get_surface()) yet, and
                # present() would crash.
                _api.warn_external("Cannot raise window yet to be setup")

    def full_screen_toggle(self):
        if not self.window.is_fullscreen():
            self.window.fullscreen()
        else:
            self.window.unfullscreen()

    def _get_toolbar(self):
        # must be inited after the window, drawingArea and figure
        # attrs are set
        if mpl.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2GTK4(self.canvas, self.window)
        elif mpl.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarGTK4(self.toolmanager)
        else:
            toolbar = None
        return toolbar

    def get_window_title(self):
        return self.window.get_title()

    def set_window_title(self, title):
        self.window.set_title(title)

    def resize(self, width, height):
        """Set the canvas size in pixels."""
        width = int(width / self.canvas.device_pixel_ratio)
        height = int(height / self.canvas.device_pixel_ratio)
        if self.toolbar:
            min_size, nat_size = self.toolbar.get_preferred_size()
            height += nat_size.height
        canvas_size = self.canvas.get_allocation()
        self.window.set_default_size(width, height)
