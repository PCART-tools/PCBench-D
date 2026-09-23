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
        if np.ndim(data) == 0 and isinstance(self, ScalarMappable):
            # This block logically belongs to ScalarMappable, but can't be
            # implemented in it because most ScalarMappable subclasses inherit
            # from Artist first and from ScalarMappable second, so
            # Artist.format_cursor_data would always have precedence over
            # ScalarMappable.format_cursor_data.
            n = self.cmap.N
            if np.ma.getmask(data):
                return "[]"
            normed = self.norm(data)
            if np.isfinite(normed):
                if isinstance(self.norm, BoundaryNorm):
                    # not an invertible normalization mapping
                    cur_idx = np.argmin(np.abs(self.norm.boundaries - data))
                    neigh_idx = max(0, cur_idx - 1)
                    # use max diff to prevent delta == 0
                    delta = np.diff(
                        self.norm.boundaries[neigh_idx:cur_idx + 2]
                    ).max()

                else:
                    # Midpoints of neighboring color intervals.
                    neighbors = self.norm.inverse(
                        (int(normed * n) + np.array([0, 1])) / n)
                    delta = abs(neighbors - data).max()
                g_sig_digits = cbook._g_sig_digits(data, delta)
            else:
                g_sig_digits = 3  # Consistent with default below.
            return "[{:-#.{}g}]".format(data, g_sig_digits)
        else:
            try:
                data[0]
            except (TypeError, IndexError):
                data = [data]
            data_str = ', '.join('{:0.3g}'.format(item) for item in data
                                 if isinstance(item, Number))
            return "[" + data_str + "]"
