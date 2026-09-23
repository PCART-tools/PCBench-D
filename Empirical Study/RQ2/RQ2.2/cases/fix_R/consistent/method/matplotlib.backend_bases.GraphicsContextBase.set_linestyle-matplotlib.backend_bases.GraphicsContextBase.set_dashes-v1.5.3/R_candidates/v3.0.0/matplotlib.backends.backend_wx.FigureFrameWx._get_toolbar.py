    def _get_toolbar(self, statbar):
        if rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2Wx(self.canvas)
            toolbar.set_status_bar(statbar)
        elif matplotlib.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarWx(self.toolmanager, self)
        else:
            toolbar = None
        return toolbar
