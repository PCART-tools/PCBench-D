class ConfigureSubplotsGTK(backend_tools.ConfigureSubplotsBase, Gtk.Window):
    def _get_canvas(self, fig):
        return self.canvas.__class__(fig)

    def trigger(self, *args):
        _NavigationToolbar2GTK.configure_subplots(
            self._make_classic_style_pseudo_toolbar(), None)
