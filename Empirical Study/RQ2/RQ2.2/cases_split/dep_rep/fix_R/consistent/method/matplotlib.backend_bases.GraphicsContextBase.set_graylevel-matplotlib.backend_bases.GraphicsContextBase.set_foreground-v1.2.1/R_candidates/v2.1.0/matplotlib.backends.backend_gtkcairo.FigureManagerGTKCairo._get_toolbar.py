    def _get_toolbar(self, canvas):
        # must be inited after the window, drawingArea and figure
        # attrs are set
        if matplotlib.rcParams['toolbar']=='toolbar2':
            toolbar = NavigationToolbar2GTKCairo (canvas, self.window)
        else:
            toolbar = None
        return toolbar
