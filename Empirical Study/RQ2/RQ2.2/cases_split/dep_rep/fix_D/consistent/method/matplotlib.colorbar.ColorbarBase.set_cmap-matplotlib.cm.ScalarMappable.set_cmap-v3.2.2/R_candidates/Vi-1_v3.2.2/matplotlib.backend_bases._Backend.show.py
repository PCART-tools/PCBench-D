    @classmethod
    @cbook._make_keyword_only("3.1", "block")
    def show(cls, block=None):
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
            # Emits a warning if the backend is non-interactive.
            manager.canvas.figure.show()
        if cls.mainloop is None:
            return
        if block is None:
            # Hack: Are we in IPython's pylab mode?
            from matplotlib import pyplot
            try:
                # IPython versions >= 0.10 tack the _needmain attribute onto
                # pyplot.show, and always set it to False, when in %pylab mode.
                ipython_pylab = not pyplot.show._needmain
            except AttributeError:
                ipython_pylab = False
            block = not ipython_pylab and not is_interactive()
            # TODO: The above is a hack to get the WebAgg backend working with
            # ipython's `%pylab` mode until proper integration is implemented.
            if get_backend() == "WebAgg":
                block = True
        if block:
            cls.mainloop()
