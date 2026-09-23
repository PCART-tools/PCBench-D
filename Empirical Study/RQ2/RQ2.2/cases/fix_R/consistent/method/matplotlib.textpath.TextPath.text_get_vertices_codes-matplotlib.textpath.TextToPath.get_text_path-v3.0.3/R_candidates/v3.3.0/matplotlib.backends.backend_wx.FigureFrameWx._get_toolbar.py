    def _get_toolbar(self):
        if mpl.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2Wx(self.canvas)
        elif mpl.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarWx(self.toolmanager, self)
        else:
            toolbar = None
        return toolbar
