class _Backend:
    # A backend can be defined by using the following pattern:
    #
    # @_Backend.export
    # class FooBackend(_Backend):
    #     # override the attributes and methods documented below.

    # `backend_version` may be overridden by the subclass.
    backend_version = "unknown"

    # The `FigureCanvas` class must be defined.
    FigureCanvas = None

    # For interactive backends, the `FigureManager` class must be overridden.
    FigureManager = FigureManagerBase

    # For interactive backends, `mainloop` should be a function taking no
    # argument and starting the backend main loop.  It should be left as None
    # for non-interactive backends.
    mainloop = None

    # The following methods will be automatically defined and exported, but
    # can be overridden.

    @classmethod
    def new_figure_manager(cls, num, *args, **kwargs):
        """Create a new figure manager instance."""
        # This import needs to happen here due to circular imports.
        from matplotlib.figure import Figure
        fig_cls = kwargs.pop('FigureClass', Figure)
        fig = fig_cls(*args, **kwargs)
        return cls.new_figure_manager_given_figure(num, fig)

    @classmethod
    def new_figure_manager_given_figure(cls, num, figure):
        """Create a new figure manager instance for the given figure."""
        canvas = cls.FigureCanvas(figure)
        manager = cls.FigureManager(canvas, num)
        return manager

    @classmethod
    def draw_if_interactive(cls):
        if cls.mainloop is not None and is_interactive():
            manager = Gcf.get_active()
            if manager:
                manager.canvas.draw_idle()

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

    # This method is the one actually exporting the required methods.

    @staticmethod
    def export(cls):
        for name in [
                "backend_version",
                "FigureCanvas",
                "FigureManager",
                "new_figure_manager",
                "new_figure_manager_given_figure",
                "draw_if_interactive",
                "show",
        ]:
            setattr(sys.modules[cls.__module__], name, getattr(cls, name))

        # For back-compatibility, generate a shim `Show` class.

        class Show(ShowBase):
            def mainloop(self):
                return cls.mainloop()

        setattr(sys.modules[cls.__module__], "Show", Show)
        return cls
