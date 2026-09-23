    def set(self, locs, values, check=False):
        """
        Modify Block in-place with new item value

        Returns
        -------
        None
        """
        if values.dtype != _NS_DTYPE:
            # Workaround for numpy 1.6 bug
            values = tslib.cast_to_nanoseconds(values)

        self.values[locs] = values
