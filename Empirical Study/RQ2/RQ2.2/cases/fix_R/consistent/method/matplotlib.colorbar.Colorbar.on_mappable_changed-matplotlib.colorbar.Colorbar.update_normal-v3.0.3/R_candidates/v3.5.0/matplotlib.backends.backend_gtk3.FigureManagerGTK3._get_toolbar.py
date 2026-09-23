    def _get_toolbar(self):
        # must be inited after the window, drawingArea and figure
        # attrs are set
        if mpl.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2GTK3(self.canvas, self.window)
        elif mpl.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarGTK3(self.toolmanager)
        else:
            toolbar = None
        return toolbar
