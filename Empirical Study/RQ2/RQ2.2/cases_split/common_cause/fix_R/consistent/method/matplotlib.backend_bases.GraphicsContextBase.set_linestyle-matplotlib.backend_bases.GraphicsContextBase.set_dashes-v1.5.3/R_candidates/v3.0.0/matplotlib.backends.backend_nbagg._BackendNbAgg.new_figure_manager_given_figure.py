    @staticmethod
    def new_figure_manager_given_figure(num, figure):
        canvas = FigureCanvasNbAgg(figure)
        manager = FigureManagerNbAgg(canvas, num)
        if is_interactive():
            manager.show()
            figure.canvas.draw_idle()
        canvas.mpl_connect('close_event', lambda event: Gcf.destroy(num))
        return manager
