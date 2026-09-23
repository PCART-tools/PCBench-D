    def _get_toolbar(self):
        if rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2Wx(self.canvas)
        elif matplotlib.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarWx(self.toolmanager, self)
        else:
            toolbar = None
        return toolbar
