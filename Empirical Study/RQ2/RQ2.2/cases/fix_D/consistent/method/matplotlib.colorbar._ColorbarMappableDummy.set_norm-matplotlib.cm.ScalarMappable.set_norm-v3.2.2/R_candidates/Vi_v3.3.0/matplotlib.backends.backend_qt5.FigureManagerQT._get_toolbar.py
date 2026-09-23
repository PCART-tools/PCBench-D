    def _get_toolbar(self, canvas, parent):
        # must be inited after the window, drawingArea and figure
        # attrs are set
        if matplotlib.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2QT(canvas, parent, True)
        elif matplotlib.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarQt(self.toolmanager, self.window)
        else:
            toolbar = None
        return toolbar
