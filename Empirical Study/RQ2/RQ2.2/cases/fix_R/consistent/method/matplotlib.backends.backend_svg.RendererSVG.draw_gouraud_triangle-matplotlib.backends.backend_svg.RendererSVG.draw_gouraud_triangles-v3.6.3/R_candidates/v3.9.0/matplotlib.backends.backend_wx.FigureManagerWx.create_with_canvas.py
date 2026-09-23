    @classmethod
    def create_with_canvas(cls, canvas_class, figure, num):
        # docstring inherited
        wxapp = wx.GetApp() or _create_wxapp()
        frame = FigureFrameWx(num, figure, canvas_class=canvas_class)
        manager = figure.canvas.manager
        if mpl.is_interactive():
            manager.frame.Show()
            figure.canvas.draw_idle()
        return manager
