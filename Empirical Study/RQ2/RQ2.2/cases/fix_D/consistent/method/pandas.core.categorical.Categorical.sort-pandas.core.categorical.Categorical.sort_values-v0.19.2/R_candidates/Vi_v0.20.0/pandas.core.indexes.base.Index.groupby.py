    def groupby(self, values):
        """
        Group the index labels by a given array of values.

        Parameters
        ----------
        values : array
            Values used to determine the groups.

        Returns
        -------
        groups : dict
            {group name -> group labels}
        """

        # TODO: if we are a MultiIndex, we can do better
        # that converting to tuples
        from .multi import MultiIndex
        if isinstance(values, MultiIndex):
            values = values.values
        values = _ensure_categorical(values)
        result = values._reverse_indexer()

        # map to the label
        result = {k: self.take(v) for k, v in compat.iteritems(result)}

        return result
