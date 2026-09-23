    def nth(self, n, dropna=None):
        """
        Take the nth row from each group if n is an int, or a subset of rows
        if n is a list of ints.

        If dropna, will take the nth non-null row, dropna is either
        Truthy (if a Series) or 'all', 'any' (if a DataFrame); this is equivalent
        to calling dropna(how=dropna) before the groupby.

        Parameters
        ----------
        n : int or list of ints
            a single nth value for the row or a list of nth values
        dropna : None or str, optional
            apply the specified dropna operation before counting which row is
            the nth row. Needs to be None, 'any' or 'all'

        Examples
        --------
        >>> df = DataFrame([[1, np.nan], [1, 4], [5, 6]], columns=['A', 'B'])
        >>> g = df.groupby('A')
        >>> g.nth(0)
           A   B
        0  1 NaN
        2  5   6
        >>> g.nth(1)
           A  B
        1  1  4
        >>> g.nth(-1)
           A  B
        1  1  4
        2  5  6
        >>> g.nth(0, dropna='any')
           B
        A
        1  4
        5  6
        >>> g.nth(1, dropna='any')  # NaNs denote group exhausted when using dropna
            B
        A
        1 NaN
        5 NaN

        """
        if isinstance(n, int):
            nth_values = [n]
        elif isinstance(n, (set, list, tuple)):
            nth_values = list(set(n))
            if dropna is not None:
                raise ValueError("dropna option with a list of nth values is not supported")
        else:
            raise TypeError("n needs to be an int or a list/set/tuple of ints")

        m = self.grouper._max_groupsize
        # filter out values that are outside [-m, m)
        pos_nth_values = [i for i in nth_values if i >= 0 and i < m]
        neg_nth_values = [i for i in nth_values if i < 0 and i >= -m]

        self._set_selection_from_grouper()
        if not dropna:  # good choice
            if not pos_nth_values and not neg_nth_values:
                # no valid nth values
                return self._selected_obj.loc[[]]

            rng = np.zeros(m, dtype=bool)
            for i in pos_nth_values:
                rng[i] = True
            is_nth = self._cumcount_array(rng)

            if neg_nth_values:
                rng = np.zeros(m, dtype=bool)
                for i in neg_nth_values:
                    rng[- i - 1] = True
                is_nth |= self._cumcount_array(rng, ascending=False)

            result = self._selected_obj[is_nth]

            # the result index
            if self.as_index:
                ax = self.obj._info_axis
                names = self.grouper.names
                if self.obj.ndim == 1:
                    # this is a pass-thru
                    pass
                elif all([ n in ax for n in names ]):
                    result.index = Index(self.obj[names][is_nth].values.ravel()).set_names(names)
                elif self._group_selection is not None:
                    result.index = self.obj._get_axis(self.axis)[is_nth]

                result = result.sort_index()

            return result

        if (isinstance(self._selected_obj, DataFrame)
           and dropna not in ['any', 'all']):
            # Note: when agg-ing picker doesn't raise this, just returns NaN
            raise ValueError("For a DataFrame groupby, dropna must be "
                             "either None, 'any' or 'all', "
                             "(was passed %s)." % (dropna),)

        # old behaviour, but with all and any support for DataFrames.
        # modified in GH 7559 to have better perf
        max_len = n if n >= 0 else - 1 - n
        dropped = self.obj.dropna(how=dropna, axis=self.axis)

        # get a new grouper for our dropped obj
        if self.keys is None and self.level is None:

            # we don't have the grouper info available (e.g. we have selected out
            # a column that is not in the current object)
            axis = self.grouper.axis
            grouper = axis[axis.isin(dropped.index)]
            keys = self.grouper.names
        else:

            # create a grouper with the original parameters, but on the dropped object
            grouper, _, _ = _get_grouper(dropped, key=self.keys, axis=self.axis,
                                         level=self.level, sort=self.sort)

        sizes = dropped.groupby(grouper).size()
        result = dropped.groupby(grouper).nth(n)
        mask = (sizes<max_len).values

        # set the results which don't meet the criteria
        if len(result) and mask.any():
            result.loc[mask] = np.nan

        # reset/reindex to the original groups
        if len(self.obj) == len(dropped) or len(result) == len(self.grouper.result_index):
            result.index = self.grouper.result_index
        else:
            result = result.reindex(self.grouper.result_index)

        return result
