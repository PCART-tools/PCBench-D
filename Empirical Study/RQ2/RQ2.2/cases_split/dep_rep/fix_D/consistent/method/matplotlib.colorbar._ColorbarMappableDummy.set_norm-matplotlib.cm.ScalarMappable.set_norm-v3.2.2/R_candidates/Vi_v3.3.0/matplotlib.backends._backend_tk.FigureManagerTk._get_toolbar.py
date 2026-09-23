    def _get_toolbar(self):
        if mpl.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        elif mpl.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarTk(self.toolmanager, self.window)
        else:
            toolbar = None
        return toolbar
