    def get_value(self, label, takeable=False):
        """
        Quickly retrieve single value at passed index label

        Parameters
        ----------
        index : label
        takeable : interpret the index as indexers, default False

        Returns
        -------
        value : scalar value
        """
        if takeable is True:
            return _maybe_box_datetimelike(self._values[label])
        return self.index.get_value(self._values, label)
