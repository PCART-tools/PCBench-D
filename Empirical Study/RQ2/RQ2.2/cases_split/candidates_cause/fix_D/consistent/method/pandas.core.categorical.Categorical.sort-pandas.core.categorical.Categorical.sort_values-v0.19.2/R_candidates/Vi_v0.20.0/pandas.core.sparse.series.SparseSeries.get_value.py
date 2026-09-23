    def get_value(self, label, takeable=False):
        """
        Retrieve single value at passed index label

        Parameters
        ----------
        index : label
        takeable : interpret the index as indexers, default False

        Returns
        -------
        value : scalar value
        """
        loc = label if takeable is True else self.index.get_loc(label)
        return self._get_val_at(loc)
