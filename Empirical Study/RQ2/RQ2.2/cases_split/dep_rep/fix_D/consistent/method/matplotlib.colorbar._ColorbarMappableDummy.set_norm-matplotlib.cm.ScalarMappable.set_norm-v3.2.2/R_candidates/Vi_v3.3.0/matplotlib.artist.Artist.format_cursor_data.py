    def format_cursor_data(self, data):
        """
        Return a string representation of *data*.

        .. note::
            This method is intended to be overridden by artist subclasses.
            As an end-user of Matplotlib you will most likely not call this
            method yourself.

        The default implementation converts ints and floats and arrays of ints
        and floats into a comma-separated string enclosed in square brackets.

        See Also
        --------
        get_cursor_data
        """
        try:
            data[0]
        except (TypeError, IndexError):
            data = [data]
        data_str = ', '.join('{:0.3g}'.format(item) for item in data
                             if isinstance(item, Number))
        return "[" + data_str + "]"
