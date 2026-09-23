    def _get_output_canvas(self, fmt):
        """
        Return a canvas suitable for saving figures to a specified file format.

        If necessary, this function will switch to a registered backend that
        supports the format.
        """
        # Return the current canvas if it supports the requested format.
        if hasattr(self, 'print_{}'.format(fmt)):
            return self
        # Return a default canvas for the requested format, if it exists.
        canvas_class = get_registered_canvas_class(fmt)
        if canvas_class:
            return self.switch_backends(canvas_class)
        # Else report error for unsupported format.
        raise ValueError(
            "Format {!r} is not supported (supported formats: {})"
            .format(fmt, ", ".join(sorted(self.get_supported_filetypes()))))
