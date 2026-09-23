    def isin(self, values):
        """
        Return boolean DataFrame showing whether each element in the
        DataFrame is contained in values.

        Parameters
        ----------
        values : iterable, Series, DataFrame or dictionary
            The result will only be true at a location if all the
            labels match. If `values` is a Series, that's the index. If
            `values` is a dictionary, the keys must be the column names,
            which must match. If `values` is a DataFrame,
            then both the index and column labels must match.

        Returns
        -------

        DataFrame of booleans

        Examples
        --------
        When ``values`` is a list:

        >>> df = DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'f']})
        >>> df.isin([1, 3, 12, 'a'])
               A      B
        0   True   True
        1  False  False
        2   True  False

        When ``values`` is a dict:

        >>> df = DataFrame({'A': [1, 2, 3], 'B': [1, 4, 7]})
        >>> df.isin({'A': [1, 3], 'B': [4, 7, 12]})
               A      B
        0   True  False  # Note that B didn't match the 1 here.
        1  False   True
        2   True   True

        When ``values`` is a Series or DataFrame:

        >>> df = DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'f']})
        >>> other = DataFrame({'A': [1, 3, 3, 2], 'B': ['e', 'f', 'f', 'e']})
        >>> df.isin(other)
               A      B
        0   True  False
        1  False  False  # Column A in `other` has a 3, but not at index 1.
        2   True   True
        """
        if isinstance(values, dict):
            from collections import defaultdict
            from pandas.tools.merge import concat
            values = defaultdict(list, values)
            return concat((self.iloc[:, [i]].isin(values[col])
                           for i, col in enumerate(self.columns)), axis=1)
        elif isinstance(values, Series):
            if not values.index.is_unique:
                raise ValueError("cannot compute isin with "
                                 "a duplicate axis.")
            return self.eq(values.reindex_like(self), axis='index')
        elif isinstance(values, DataFrame):
            if not (values.columns.is_unique and values.index.is_unique):
                raise ValueError("cannot compute isin with "
                                 "a duplicate axis.")
            return self.eq(values.reindex_like(self))
        else:
            if not is_list_like(values):
                raise TypeError("only list-like or dict-like objects are "
                                "allowed to be passed to DataFrame.isin(), "
                                "you passed a "
                                "{0!r}".format(type(values).__name__))
            return DataFrame(lib.ismember(self.values.ravel(),
                             set(values)).reshape(self.shape), self.index,
                             self.columns)
