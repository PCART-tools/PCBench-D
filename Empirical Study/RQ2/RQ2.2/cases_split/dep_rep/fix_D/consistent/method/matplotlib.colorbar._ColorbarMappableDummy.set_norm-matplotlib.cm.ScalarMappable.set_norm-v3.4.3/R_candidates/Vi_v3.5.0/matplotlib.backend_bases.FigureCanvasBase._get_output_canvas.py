    def _get_output_canvas(self, backend, fmt):
        """
        Set the canvas in preparation for saving the figure.

        Parameters
        ----------
        backend : str or None
            If not None, switch the figure canvas to the ``FigureCanvas`` class
            of the given backend.
        fmt : str
            If *backend* is None, then determine a suitable canvas class for
            saving to format *fmt* -- either the current canvas class, if it
            supports *fmt*, or whatever `get_registered_canvas_class` returns;
            switch the figure canvas to that canvas class.
        """
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
            return self
        else:
            # Return a default canvas for the requested format, if it exists.
            canvas_class = get_registered_canvas_class(fmt)
        if canvas_class:
            return self.switch_backends(canvas_class)
        # Else report error for unsupported format.
        raise ValueError(
            "Format {!r} is not supported (supported formats: {})"
            .format(fmt, ", ".join(sorted(self.get_supported_filetypes()))))
