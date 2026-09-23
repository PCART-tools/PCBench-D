    def set(self, item, value, check=False):
        """
        Modify Block in-place with new item value

        Returns
        -------
        None
        """
        loc = self.items.get_loc(item)

        if value.dtype != _NS_DTYPE:
            value = tslib.cast_to_nanoseconds(value)

        self.values[loc] = value
