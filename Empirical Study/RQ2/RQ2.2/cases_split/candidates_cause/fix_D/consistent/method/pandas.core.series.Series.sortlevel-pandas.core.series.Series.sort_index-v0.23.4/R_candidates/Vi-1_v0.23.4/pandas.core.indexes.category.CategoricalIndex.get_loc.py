    def get_loc(self, key, method=None):
        """
        Get integer location, slice or boolean mask for requested label.

        Parameters
        ----------
        key : label
        method : {None}
            * default: exact matches only.

        Returns
        -------
        loc : int if unique index, slice if monotonic index, else mask

        Examples
        ---------
        >>> unique_index = pd.CategoricalIndex(list('abc'))
        >>> unique_index.get_loc('b')
        1

        >>> monotonic_index = pd.CategoricalIndex(list('abbc'))
        >>> monotonic_index.get_loc('b')
        slice(1, 3, None)

        >>> non_monotonic_index = p.dCategoricalIndex(list('abcb'))
        >>> non_monotonic_index.get_loc('b')
        array([False,  True, False,  True], dtype=bool)
        """
        codes = self.categories.get_loc(key)
        if (codes == -1):
            raise KeyError(key)
        return self._engine.get_loc(codes)
