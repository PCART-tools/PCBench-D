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
            Take the last observed row in a row. Defaults to the first row
        cols : kwargs only argument of subset [deprecated]

        Returns
        -------
        duplicated : Series
        """
        # kludge for #1833
        def _m8_to_i8(x):
            if issubclass(x.dtype.type, np.datetime64):
                return x.view(np.int64)
            return x

        if subset is None:
            values = list(_m8_to_i8(self.values.T))
        else:
            if np.iterable(subset) and not isinstance(subset, compat.string_types):
                if isinstance(subset, tuple):
                    if subset in self.columns:
                        values = [self[subset].values]
                    else:
                        values = [_m8_to_i8(self[x].values) for x in subset]
                else:
                    values = [_m8_to_i8(self[x].values) for x in subset]
            else:
                values = [self[subset].values]

        keys = lib.fast_zip_fillna(values)
        duplicated = lib.duplicated(keys, take_last=take_last)
        return Series(duplicated, index=self.index)
