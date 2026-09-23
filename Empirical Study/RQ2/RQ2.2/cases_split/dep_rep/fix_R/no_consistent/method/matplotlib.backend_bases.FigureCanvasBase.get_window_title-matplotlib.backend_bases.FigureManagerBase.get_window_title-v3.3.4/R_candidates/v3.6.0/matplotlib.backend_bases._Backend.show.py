    @classmethod
    def show(cls, *, block=None):
        """
        Show all figures.

        `show` blocks by calling `mainloop` if *block* is ``True``, or if it
        is ``None`` and we are neither in IPython's ``%pylab`` mode, nor in
        `interactive` mode.
        """
        managers = Gcf.get_all_fig_managers()
        if not managers:
            return
        for manager in managers:
            try:
                manager.show()  # Emits a warning for non-interactive backend.
            except NonGuiException as exc:
                _api.warn_external(str(exc))
        if cls.mainloop is None:
            return
        if block is None:
            # Hack: Are we in IPython's %pylab mode?  In pylab mode, IPython
            # (>= 0.10) tacks a _needmain attribute onto pyplot.show (always
            # set to False).
            from matplotlib import pyplot
            ipython_pylab = hasattr(pyplot.show, "_needmain")
            block = not ipython_pylab and not is_interactive()
        if block:
            cls.mainloop()
