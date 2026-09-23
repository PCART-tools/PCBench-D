class ToolbarGTK3(ToolContainerBase, Gtk.Box):
    _icon_extension = '.png'

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

    def add_toolitem(self, name, group, position, image_file, description,
                     toggle):
        if toggle:
            tbutton = Gtk.ToggleToolButton()
        else:
            tbutton = Gtk.ToolButton()
        tbutton.set_label(name)

        if image_file is not None:
            image = Gtk.Image()
            image.set_from_file(image_file)
            tbutton.set_icon_widget(image)

        if position is None:
            position = -1

        self._add_button(tbutton, group, position)
        signal = tbutton.connect('clicked', self._call_tool, name)
        tbutton.set_tooltip_text(description)
        tbutton.show_all()
        self._toolitems.setdefault(name, [])
        self._toolitems[name].append((tbutton, signal))

    def _add_button(self, button, group, position):
        if group not in self._groups:
            if self._groups:
                self._add_separator()
            toolbar = Gtk.Toolbar()
            toolbar.set_style(Gtk.ToolbarStyle.ICONS)
            self._toolarea.pack_start(toolbar, False, False, 0)
            toolbar.show_all()
            self._groups[group] = toolbar
        self._groups[group].insert(button, position)

    def _call_tool(self, btn, name):
        self.trigger_tool(name)

    def toggle_toolitem(self, name, toggled):
        if name not in self._toolitems:
            return
        for toolitem, signal in self._toolitems[name]:
            toolitem.handler_block(signal)
            toolitem.set_active(toggled)
            toolitem.handler_unblock(signal)

    def remove_toolitem(self, name):
        if name not in self._toolitems:
            self.toolmanager.message_event('%s Not in toolbar' % name, self)
            return

        for group in self._groups:
            for toolitem, _signal in self._toolitems[name]:
                if toolitem in self._groups[group]:
                    self._groups[group].remove(toolitem)
        del self._toolitems[name]

    def _add_separator(self):
        sep = Gtk.Separator()
        sep.set_property("orientation", Gtk.Orientation.VERTICAL)
        self._toolarea.pack_start(sep, False, True, 0)
        sep.show_all()
