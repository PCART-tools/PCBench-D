    def __init__(self, canvas, num):
        _macosx.FigureManager.__init__(self, canvas)
        FigureManagerBase.__init__(self, canvas, num)
        if mpl.rcParams['toolbar'] == 'toolbar2':
            self.toolbar = NavigationToolbar2Mac(canvas)
        else:
            self.toolbar = None
        if self.toolbar is not None:
            self.toolbar.update()

        if mpl.is_interactive():
            self.show()
            self.canvas.draw_idle()
