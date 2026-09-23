    def add_toolitem(self, name, group, position, image_file, description,
                     toggle):
        if toggle:
            button = Gtk.ToggleToolButton()
        else:
            button = Gtk.ToolButton()
        button.set_label(name)

        if image_file is not None:
            image = Gtk.Image.new_from_gicon(
                Gio.Icon.new_for_string(image_file),
                Gtk.IconSize.LARGE_TOOLBAR)
            button.set_icon_widget(image)

        if position is None:
            position = -1

        self._add_button(button, group, position)
        signal = button.connect('clicked', self._call_tool, name)
        button.set_tooltip_text(description)
        button.show_all()
        self._toolitems.setdefault(name, [])
        self._toolitems[name].append((button, signal))
