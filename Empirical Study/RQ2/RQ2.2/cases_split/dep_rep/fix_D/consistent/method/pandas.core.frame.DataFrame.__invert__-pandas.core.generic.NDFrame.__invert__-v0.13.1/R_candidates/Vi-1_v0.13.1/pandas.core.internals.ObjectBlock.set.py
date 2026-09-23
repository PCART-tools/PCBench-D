    def set(self, item, value, check=False):
        """
        Modify Block in-place with new item value

        Returns
        -------
        None
        """

        loc = self.items.get_loc(item)

        # GH6026
        if check:
            try:
                if (self.values[loc] == value).all():
                    return
            except:
                pass
        try:
            self.values[loc] = value
        except (ValueError):

            # broadcasting error
            # see GH6171
            new_shape = list(value.shape)
            new_shape[0] = len(self.items)
            self.values = np.empty(tuple(new_shape),dtype=self.dtype)
            self.values.fill(np.nan)
            self.values[loc] = value
