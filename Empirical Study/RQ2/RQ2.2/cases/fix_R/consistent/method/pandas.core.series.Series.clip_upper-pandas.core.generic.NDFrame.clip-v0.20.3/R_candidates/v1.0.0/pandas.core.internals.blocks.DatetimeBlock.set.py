    def set(self, locs, values):
        """
        Modify Block in-place with new item value

        Returns
        -------
        None
        """
        values = conversion.ensure_datetime64ns(values, copy=False)

        self.values[locs] = values
