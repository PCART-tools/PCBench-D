    @deprecate_kwarg(old_arg_name='cols', new_arg_name='subset')
    def duplicated(self, subset=None, take_last=False):
        """
        Return boolean Series denoting duplicate rows, optionally only
        considering certain columns

        Parameters
        ----------
        subset : column label or sequence of labels, optional
            Only consider certain columns for identifying duplicates, by
            default use all of the columns
        take_last : boolean, default False
            For a set of distinct duplicate rows, flag all but the last row as
            duplicated. Default is for all but the first row to be flagged
        cols : kwargs only argument of subset [deprecated]

        Returns
        -------
        duplicated : Series
        """
        from pandas.core.groupby import get_group_index
        from pandas.core.algorithms import factorize
        from pandas.hashtable import duplicated_int64, _SIZE_HINT_LIMIT

        def f(vals):
            labels, shape = factorize(vals, size_hint=min(len(self), _SIZE_HINT_LIMIT))
            return labels.astype('i8',copy=False), len(shape)

        if subset is None:
            subset = self.columns
        elif not np.iterable(subset) or \
                isinstance(subset, compat.string_types) or \
                isinstance(subset, tuple) and subset in self.columns:
            subset = subset,

        vals = (self[col].values for col in subset)
        labels, shape = map(list, zip( * map(f, vals)))

        ids = get_group_index(labels, shape, sort=False, xnull=False)
        return Series(duplicated_int64(ids, take_last), index=self.index)
