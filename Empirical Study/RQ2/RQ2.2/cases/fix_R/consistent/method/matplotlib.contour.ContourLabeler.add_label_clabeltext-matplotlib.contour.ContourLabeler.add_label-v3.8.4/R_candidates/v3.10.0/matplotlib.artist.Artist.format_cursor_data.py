    def format_cursor_data(self, data):
        """
        Return a string representation of *data*.

        .. note::
            This method is intended to be overridden by artist subclasses.
            As an end-user of Matplotlib you will most likely not call this
            method yourself.

        The default implementation converts ints and floats and arrays of ints
        and floats into a comma-separated string enclosed in square brackets,
        unless the artist has an associated colorbar, in which case scalar
        values are formatted using the colorbar's formatter.

        See Also
        --------
        get_cursor_data
        """
        if np.ndim(data) == 0 and hasattr(self, "_format_cursor_data_override"):
            # workaround for ScalarMappable to be able to define its own
            # format_cursor_data(). See ScalarMappable._format_cursor_data_override
            # for details.
            return self._format_cursor_data_override(data)
        else:
            try:
                data[0]
            except (TypeError, IndexError):
                data = [data]
            data_str = ', '.join(f'{item:0.3g}' for item in data
                                 if isinstance(item, Number))
            return "[" + data_str + "]"
