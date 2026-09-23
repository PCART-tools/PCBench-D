    def _get_output_canvas(self, format):
        """Return a canvas that is suitable for saving figures to a specified
        file format. If necessary, this function will switch to a registered
        backend that supports the format.
        """
        method_name = 'print_%s' % format

        # check if this canvas supports the requested format
        if hasattr(self, method_name):
            return self

        # check if there is a default canvas for the requested format
        canvas_class = get_registered_canvas_class(format)
        if canvas_class:
            return self.switch_backends(canvas_class)

        # else report error for unsupported format
        formats = sorted(self.get_supported_filetypes())
        raise ValueError('Format "%s" is not supported.\n'
                         'Supported formats: '
                         '%s.' % (format, ', '.join(formats)))
