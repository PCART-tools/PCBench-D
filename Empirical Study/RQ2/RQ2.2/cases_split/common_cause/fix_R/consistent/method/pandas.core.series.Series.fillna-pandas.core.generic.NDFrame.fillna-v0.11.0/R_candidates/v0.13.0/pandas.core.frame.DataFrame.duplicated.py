    def duplicated(self, cols=None, take_last=False):
        """
        Return boolean Series denoting duplicate rows, optionally only
        considering certain columns

        Parameters
        ----------
        cols : column label or sequence of labels, optional
            Only consider certain columns for identifying duplicates, by
            default use all of the columns
        take_last : boolean, default False
            Take the last observed row in a row. Defaults to the first row

        Returns
        -------
        duplicated : Series
        """
        # kludge for #1833
        def _m8_to_i8(x):
            if issubclass(x.dtype.type, np.datetime64):
                return x.view(np.int64)
            return x

        if cols is None:
            values = list(_m8_to_i8(self.values.T))
        else:
            if np.iterable(cols) and not isinstance(cols, compat.string_types):
                if isinstance(cols, tuple):
                    if cols in self.columns:
                        values = [self[cols].values]
                    else:
                        values = [_m8_to_i8(self[x].values) for x in cols]
                else:
                    values = [_m8_to_i8(self[x].values) for x in cols]
            else:
                values = [self[cols].values]

        keys = lib.fast_zip_fillna(values)
        duplicated = lib.duplicated(keys, take_last=take_last)
        return Series(duplicated, index=self.index)
