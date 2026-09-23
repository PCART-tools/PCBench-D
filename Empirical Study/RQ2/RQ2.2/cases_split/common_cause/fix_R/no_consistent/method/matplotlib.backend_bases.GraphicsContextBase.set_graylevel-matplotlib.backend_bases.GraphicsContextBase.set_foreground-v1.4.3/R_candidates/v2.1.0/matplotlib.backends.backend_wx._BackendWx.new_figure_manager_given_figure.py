    @classmethod
    def new_figure_manager_given_figure(cls, num, figure):
        frame = cls._frame_class(num, figure)
        figmgr = frame.get_figure_manager()
        if matplotlib.is_interactive():
            figmgr.frame.Show()
            figure.canvas.draw_idle()
        return figmgr
