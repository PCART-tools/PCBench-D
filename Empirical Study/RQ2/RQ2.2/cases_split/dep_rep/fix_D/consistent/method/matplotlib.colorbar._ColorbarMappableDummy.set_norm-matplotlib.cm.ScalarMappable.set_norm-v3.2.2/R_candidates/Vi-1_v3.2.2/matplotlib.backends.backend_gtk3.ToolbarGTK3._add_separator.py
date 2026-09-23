    def _add_separator(self):
        sep = Gtk.Separator()
        sep.set_property("orientation", Gtk.Orientation.VERTICAL)
        self._toolarea.pack_start(sep, False, True, 0)
        sep.show_all()
