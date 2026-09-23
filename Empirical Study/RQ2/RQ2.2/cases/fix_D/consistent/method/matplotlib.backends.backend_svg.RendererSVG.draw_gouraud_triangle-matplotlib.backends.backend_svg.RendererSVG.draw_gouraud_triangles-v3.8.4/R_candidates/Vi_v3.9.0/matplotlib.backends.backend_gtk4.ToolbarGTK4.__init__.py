    def __init__(self, toolmanager):
        ToolContainerBase.__init__(self, toolmanager)
        Gtk.Box.__init__(self)
        self.set_property('orientation', Gtk.Orientation.HORIZONTAL)

        # Tool items are created later, but must appear before the message.
        self._tool_box = Gtk.Box()
        self.append(self._tool_box)
        self._groups = {}
        self._toolitems = {}

        # This filler item ensures the toolbar is always at least two text
        # lines high. Otherwise the canvas gets redrawn as the mouse hovers
        # over images because those use two-line messages which resize the
        # toolbar.
        label = Gtk.Label()
        label.set_markup(
            '<small>\N{NO-BREAK SPACE}\n\N{NO-BREAK SPACE}</small>')
        label.set_hexpand(True)  # Push real message to the right.
        self.append(label)

        self._message = Gtk.Label()
        self._message.set_justify(Gtk.Justification.RIGHT)
        self.append(self._message)
