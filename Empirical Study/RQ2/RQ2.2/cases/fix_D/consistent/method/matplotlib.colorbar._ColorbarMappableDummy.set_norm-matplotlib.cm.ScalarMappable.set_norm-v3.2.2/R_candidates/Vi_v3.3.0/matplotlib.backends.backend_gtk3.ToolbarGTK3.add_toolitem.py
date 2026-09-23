    def add_toolitem(self, name, group, position, image_file, description,
                     toggle):
        if toggle:
            tbutton = Gtk.ToggleToolButton()
        else:
            tbutton = Gtk.ToolButton()
        tbutton.set_label(name)

        if image_file is not None:
            image = Gtk.Image.new_from_gicon(
                Gio.Icon.new_for_string(image_file),
                Gtk.IconSize.LARGE_TOOLBAR)
            tbutton.set_icon_widget(image)

        if position is None:
            position = -1

        self._add_button(tbutton, group, position)
        signal = tbutton.connect('clicked', self._call_tool, name)
        tbutton.set_tooltip_text(description)
        tbutton.show_all()
        self._toolitems.setdefault(name, [])
        self._toolitems[name].append((tbutton, signal))
