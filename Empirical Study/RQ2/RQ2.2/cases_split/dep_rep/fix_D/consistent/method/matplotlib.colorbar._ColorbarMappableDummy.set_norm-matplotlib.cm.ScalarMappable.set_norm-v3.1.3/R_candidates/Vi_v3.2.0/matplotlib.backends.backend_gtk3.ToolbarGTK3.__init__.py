    def __init__(self, toolmanager):
        ToolContainerBase.__init__(self, toolmanager)
        Gtk.Box.__init__(self)
        self.set_property("orientation", Gtk.Orientation.VERTICAL)

        self._toolarea = Gtk.Box()
        self._toolarea.set_property('orientation', Gtk.Orientation.HORIZONTAL)
        self.pack_start(self._toolarea, False, False, 0)
        self._toolarea.show_all()
        self._groups = {}
        self._toolitems = {}
