    @staticmethod
    def show(*args, block=None, **kwargs):
        if args or kwargs:
            cbook.warn_deprecated(
                "3.1", message="Passing arguments to show(), other than "
                "passing 'block' by keyword, is deprecated %(since)s, and "
                "support for it will be removed %(removal)s.")

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
