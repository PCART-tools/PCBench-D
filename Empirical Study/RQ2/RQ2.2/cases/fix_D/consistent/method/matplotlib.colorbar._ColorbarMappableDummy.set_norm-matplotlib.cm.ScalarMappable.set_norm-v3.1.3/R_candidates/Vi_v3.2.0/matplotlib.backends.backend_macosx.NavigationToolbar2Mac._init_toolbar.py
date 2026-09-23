    def _init_toolbar(self):
        _macosx.NavigationToolbar2.__init__(
            self, str(cbook._get_data_path('images')))
