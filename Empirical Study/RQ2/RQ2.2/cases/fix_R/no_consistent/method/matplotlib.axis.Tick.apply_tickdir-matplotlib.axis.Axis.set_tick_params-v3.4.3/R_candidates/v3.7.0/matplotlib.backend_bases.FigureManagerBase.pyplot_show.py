    @classmethod
    def pyplot_show(cls, *, block=None):
        """
        Show all figures.  This method is the implementation of `.pyplot.show`.

        To customize the behavior of `.pyplot.show`, interactive backends
        should usually override `~.FigureManagerBase.start_main_loop`; if more
        customized logic is necessary, `~.FigureManagerBase.pyplot_show` can
        also be overridden.

        Parameters
        ----------
        block : bool, optional
            Whether to block by calling ``start_main_loop``.  The default,
            None, means to block if we are neither in IPython's ``%pylab`` mode
            nor in ``interactive`` mode.
        """
        managers = Gcf.get_all_fig_managers()
        if not managers:
            return
        for manager in managers:
            try:
                manager.show()  # Emits a warning for non-interactive backend.
            except NonGuiException as exc:
                _api.warn_external(str(exc))
        if block is None:
            # Hack: Are we in IPython's %pylab mode?  In pylab mode, IPython
            # (>= 0.10) tacks a _needmain attribute onto pyplot.show (always
            # set to False).
            ipython_pylab = hasattr(
                getattr(sys.modules.get("pyplot"), "show", None), "_needmain")
            block = not ipython_pylab and not is_interactive()
        if block:
            cls.start_main_loop()
