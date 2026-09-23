    def _get_toolbar(self, canvas, parent):
        # must be inited after the window, drawingArea and figure
        # attrs are set
        if mpl.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2QT(canvas, parent, True)
        elif mpl.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarQt(self.toolmanager, self.window)
        else:
            toolbar = None
        return toolbar
