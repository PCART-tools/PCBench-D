    def __init__(self, canvas, num):
        self._shown = False
        _macosx.FigureManager.__init__(self, canvas)
        icon_path = str(cbook._get_data_path('images/matplotlib.pdf'))
        _macosx.FigureManager.set_icon(icon_path)
        FigureManagerBase.__init__(self, canvas, num)
        self._set_window_mode(mpl.rcParams.get("macosx.window_mode", "system"))
        if self.toolbar is not None:
            self.toolbar.update()
        if mpl.is_interactive():
            self.show()
            self.canvas.draw_idle()
