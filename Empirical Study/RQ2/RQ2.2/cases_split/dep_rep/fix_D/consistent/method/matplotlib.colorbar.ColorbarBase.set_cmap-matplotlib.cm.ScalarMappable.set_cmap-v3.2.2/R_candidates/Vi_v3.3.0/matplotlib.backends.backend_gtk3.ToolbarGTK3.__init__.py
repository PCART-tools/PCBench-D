    def __init__(self, toolmanager):
        ToolContainerBase.__init__(self, toolmanager)
        Gtk.Box.__init__(self)
        self.set_property('orientation', Gtk.Orientation.HORIZONTAL)
        self._message = Gtk.Label()
        self.pack_end(self._message, False, False, 0)
        self.show_all()
        self._groups = {}
        self._toolitems = {}
