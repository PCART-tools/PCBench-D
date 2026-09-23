@_Backend.export
class _BackendNbAgg(_Backend):
    FigureCanvas = FigureCanvasNbAgg
    FigureManager = FigureManagerNbAgg

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

    @staticmethod
    def show(block=None):
        ## TODO: something to do when keyword block==False ?
        from matplotlib._pylab_helpers import Gcf

        managers = Gcf.get_all_fig_managers()
        if not managers:
            return

        interactive = is_interactive()

        for manager in managers:
            manager.show()

            # plt.figure adds an event which makes the figure in focus the
            # active one. Disable this behaviour, as it results in
            # figures being put as the active figure after they have been
            # shown, even in non-interactive mode.
            if hasattr(manager, '_cidgcf'):
                manager.canvas.mpl_disconnect(manager._cidgcf)

            if not interactive:
                Gcf.figs.pop(manager.num, None)
