    def _show_shortcuts_dialog(self):
        dialog = Gtk.MessageDialog(
            self._figure.canvas.get_toplevel(),
            0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, self._get_help_text(),
            title="Help")
        dialog.run()
        dialog.destroy()
