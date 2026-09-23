    def to_series(self, index=None, name=None):
        """
        Create a Series with both index and values equal to the index keys.

        Useful with map for returning an indexer based on an index.

        Parameters
        ----------
        index : Index, optional
            Index of resulting Series. If None, defaults to original index.
        name : str, optional
            Dame of resulting Series. If None, defaults to name of original
            index.

        Returns
        -------
        Series
            The dtype will be based on the type of the Index values.
        """

        from pandas import Series

        if index is None:
            index = self._shallow_copy()
        if name is None:
            name = self.name

        return Series(self.values.copy(), index=index, name=name)
