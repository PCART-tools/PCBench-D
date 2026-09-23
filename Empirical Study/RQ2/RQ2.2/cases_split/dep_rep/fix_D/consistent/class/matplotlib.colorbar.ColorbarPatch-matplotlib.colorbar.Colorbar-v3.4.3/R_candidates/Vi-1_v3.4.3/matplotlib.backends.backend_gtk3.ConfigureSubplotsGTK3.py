class ConfigureSubplotsGTK3(backend_tools.ConfigureSubplotsBase, Gtk.Window):
    def _get_canvas(self, fig):
        return self.canvas.__class__(fig)

    def trigger(self, *args):
        NavigationToolbar2GTK3.configure_subplots(
            self._make_classic_style_pseudo_toolbar(), None)
