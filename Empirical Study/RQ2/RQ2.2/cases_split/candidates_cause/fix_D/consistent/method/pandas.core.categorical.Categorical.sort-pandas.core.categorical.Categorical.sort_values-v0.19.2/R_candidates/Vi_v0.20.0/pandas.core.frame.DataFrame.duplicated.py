    def duplicated(self, subset=None, keep='first'):
        """
        Return boolean Series denoting duplicate rows, optionally only
        considering certain columns

        Parameters
        ----------
        subset : column label or sequence of labels, optional
            Only consider certain columns for identifying duplicates, by
            default use all of the columns
        keep : {'first', 'last', False}, default 'first'
            - ``first`` : Mark duplicates as ``True`` except for the
              first occurrence.
            - ``last`` : Mark duplicates as ``True`` except for the
              last occurrence.
            - False : Mark all duplicates as ``True``.

        Returns
        -------
        duplicated : Series
        """
        from pandas.core.sorting import get_group_index
        from pandas._libs.hashtable import duplicated_int64, _SIZE_HINT_LIMIT

        def f(vals):
            labels, shape = algorithms.factorize(
                vals, size_hint=min(len(self), _SIZE_HINT_LIMIT))
            return labels.astype('i8', copy=False), len(shape)

        if subset is None:
            subset = self.columns
        elif (not np.iterable(subset) or
              isinstance(subset, compat.string_types) or
              isinstance(subset, tuple) and subset in self.columns):
            subset = subset,

        vals = (self[col].values for col in subset)
        labels, shape = map(list, zip(*map(f, vals)))

        ids = get_group_index(labels, shape, sort=False, xnull=False)
        return Series(duplicated_int64(ids, keep), index=self.index)
