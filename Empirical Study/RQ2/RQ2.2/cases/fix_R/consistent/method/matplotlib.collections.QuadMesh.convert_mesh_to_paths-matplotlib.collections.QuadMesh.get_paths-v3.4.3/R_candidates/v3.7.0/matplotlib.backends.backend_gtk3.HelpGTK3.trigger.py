    def trigger(self, *args):
        if Gtk.check_version(3, 20, 0) is None:
            self._show_shortcuts_window()
        else:
            self._show_shortcuts_dialog()
