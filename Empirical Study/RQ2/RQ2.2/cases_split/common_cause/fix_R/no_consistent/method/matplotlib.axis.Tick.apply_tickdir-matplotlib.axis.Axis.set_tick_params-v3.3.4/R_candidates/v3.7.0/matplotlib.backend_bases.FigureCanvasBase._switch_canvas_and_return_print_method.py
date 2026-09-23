    @contextmanager
    def _switch_canvas_and_return_print_method(self, fmt, backend=None):
        """
        Context manager temporarily setting the canvas for saving the figure::

            with canvas._switch_canvas_and_return_print_method(fmt, backend) \\
                    as print_method:
                # ``print_method`` is a suitable ``print_{fmt}`` method, and
                # the figure's canvas is temporarily switched to the method's
                # canvas within the with... block.  ``print_method`` is also
                # wrapped to suppress extra kwargs passed by ``print_figure``.

        Parameters
        ----------
        fmt : str
            If *backend* is None, then determine a suitable canvas class for
            saving to format *fmt* -- either the current canvas class, if it
            supports *fmt*, or whatever `get_registered_canvas_class` returns;
            switch the figure canvas to that canvas class.
        backend : str or None, default: None
            If not None, switch the figure canvas to the ``FigureCanvas`` class
            of the given backend.
        """
        canvas = None
        if backend is not None:
            # Return a specific canvas class, if requested.
            canvas_class = (
                importlib.import_module(cbook._backend_module_name(backend))
                .FigureCanvas)
            if not hasattr(canvas_class, f"print_{fmt}"):
                raise ValueError(
                    f"The {backend!r} backend does not support {fmt} output")
        elif hasattr(self, f"print_{fmt}"):
            # Return the current canvas if it supports the requested format.
            canvas = self
            canvas_class = None  # Skip call to switch_backends.
        else:
            # Return a default canvas for the requested format, if it exists.
            canvas_class = get_registered_canvas_class(fmt)
        if canvas_class:
            canvas = self.switch_backends(canvas_class)
        if canvas is None:
            raise ValueError(
                "Format {!r} is not supported (supported formats: {})".format(
                    fmt, ", ".join(sorted(self.get_supported_filetypes()))))
        meth = getattr(canvas, f"print_{fmt}")
        mod = (meth.func.__module__
               if hasattr(meth, "func")  # partialmethod, e.g. backend_wx.
               else meth.__module__)
        if mod.startswith(("matplotlib.", "mpl_toolkits.")):
            optional_kws = {  # Passed by print_figure for other renderers.
                "dpi", "facecolor", "edgecolor", "orientation",
                "bbox_inches_restore"}
            skip = optional_kws - {*inspect.signature(meth).parameters}
            print_method = functools.wraps(meth)(lambda *args, **kwargs: meth(
                *args, **{k: v for k, v in kwargs.items() if k not in skip}))
        else:  # Let third-parties do as they see fit.
            print_method = meth
        try:
            yield print_method
        finally:
            self.figure.canvas = self
