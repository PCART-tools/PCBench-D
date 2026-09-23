    def set(self, locs, values, check=False):
        """
        Modify Block in-place with new item value

        Returns
        -------
        None
        """

        # GH6026
        if check:
            try:
                if (self.values[locs] == values).all():
                    return
            except:
                pass
        try:
            self.values[locs] = values
        except (ValueError):

            # broadcasting error
            # see GH6171
            new_shape = list(values.shape)
            new_shape[0] = len(self.items)
            self.values = np.empty(tuple(new_shape),dtype=self.dtype)
            self.values.fill(np.nan)
            self.values[locs] = values
