    def __init__(self, canvas, num):
        FigureManagerBase.__init__(self, canvas, num)
        title = "Figure %d" % num
        _macosx.FigureManager.__init__(self, canvas, title)
        if rcParams['toolbar']=='toolbar2':
            self.toolbar = NavigationToolbar2Mac(canvas)
        else:
            self.toolbar = None
        if self.toolbar is not None:
            self.toolbar.update()

        def notify_axes_change(fig):
            'this will be called whenever the current axes is changed'
            if self.toolbar != None: self.toolbar.update()
        self.canvas.figure.add_axobserver(notify_axes_change)

        if matplotlib.is_interactive():
            self.show()
            self.canvas.draw_idle()
