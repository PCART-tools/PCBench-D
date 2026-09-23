    @staticmethod
    def new_figure_manager_given_figure(num, figure):
        canvas = FigureCanvasNbAgg(figure)
        manager = FigureManagerNbAgg(canvas, num)
        if is_interactive():
            manager.show()
            figure.canvas.draw_idle()

        def destroy(event):
            canvas.mpl_disconnect(cid)
            Gcf.destroy(manager)

        cid = canvas.mpl_connect('close_event', destroy)
        return manager
