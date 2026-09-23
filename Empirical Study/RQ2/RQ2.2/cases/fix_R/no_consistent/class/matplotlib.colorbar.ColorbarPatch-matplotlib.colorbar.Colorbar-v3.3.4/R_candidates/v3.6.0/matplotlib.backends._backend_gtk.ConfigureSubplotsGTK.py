class ConfigureSubplotsGTK(backend_tools.ConfigureSubplotsBase):
    def trigger(self, *args):
        _NavigationToolbar2GTK.configure_subplots(self, None)
