    @Substitution(name='groupby')
    @Appender(_doc_template)
    def nth(self, n, dropna=None):
        """
        Take the nth row from each group if n is an int, or a subset of rows
        if n is a list of ints.

        If dropna, will take the nth non-null row, dropna is either
        Truthy (if a Series) or 'all', 'any' (if a DataFrame);
        this is equivalent to calling dropna(how=dropna) before the
        groupby.

        Parameters
        ----------
        n : int or list of ints
            a single nth value for the row or a list of nth values
        dropna : None or str, optional
            apply the specified dropna operation before counting which row is
            the nth row. Needs to be None, 'any' or 'all'

        Examples
        --------

        >>> df = pd.DataFrame({'A': [1, 1, 2, 1, 2],
        ...                    'B': [np.nan, 2, 3, 4, 5]}, columns=['A', 'B'])
        >>> g = df.groupby('A')
        >>> g.nth(0)
             B
        A
        1  NaN
        2  3.0
        >>> g.nth(1)
             B
        A
        1  2.0
        2  5.0
        >>> g.nth(-1)
             B
        A
        1  4.0
        2  5.0
        >>> g.nth([0, 1])
             B
        A
        1  NaN
        1  2.0
        2  3.0
        2  5.0

        Specifying ``dropna`` allows count ignoring NaN

        >>> g.nth(0, dropna='any')
             B
        A
        1  2.0
        2  3.0

        NaNs denote group exhausted when using dropna

        >>> g.nth(3, dropna='any')
            B
        A
        1 NaN
        2 NaN

        Specifying ``as_index=False`` in ``groupby`` keeps the original index.

        >>> df.groupby('A', as_index=False).nth(1)
           A    B
        1  1  2.0
        4  2  5.0
        """

        if isinstance(n, int):
            nth_values = [n]
        elif isinstance(n, (set, list, tuple)):
            nth_values = list(set(n))
            if dropna is not None:
                raise ValueError(
                    "dropna option with a list of nth values is not supported")
        else:
            raise TypeError("n needs to be an int or a list/set/tuple of ints")

        nth_values = np.array(nth_values, dtype=np.intp)
        self._set_group_selection()

        if not dropna:
            mask = np.in1d(self._cumcount_array(), nth_values) | \
                np.in1d(self._cumcount_array(ascending=False) + 1, -nth_values)

            out = self._selected_obj[mask]
            if not self.as_index:
                return out

            ids, _, _ = self.grouper.group_info
            out.index = self.grouper.result_index[ids[mask]]

            return out.sort_index() if self.sort else out

        if dropna not in ['any', 'all']:
            if isinstance(self._selected_obj, Series) and dropna is True:
                warnings.warn("the dropna={dropna} keyword is deprecated,"
                              "use dropna='all' instead. "
                              "For a Series groupby, dropna must be "
                              "either None, 'any' or 'all'.".format(
                                  dropna=dropna),
                              FutureWarning,
                              stacklevel=2)
                dropna = 'all'
            else:
                # Note: when agg-ing picker doesn't raise this,
                # just returns NaN
                raise ValueError("For a DataFrame groupby, dropna must be "
                                 "either None, 'any' or 'all', "
                                 "(was passed %s)." % (dropna),)

        # old behaviour, but with all and any support for DataFrames.
        # modified in GH 7559 to have better perf
        max_len = n if n >= 0 else - 1 - n
        dropped = self.obj.dropna(how=dropna, axis=self.axis)

        # get a new grouper for our dropped obj
        if self.keys is None and self.level is None:

            # we don't have the grouper info available
            # (e.g. we have selected out
            # a column that is not in the current object)
            axis = self.grouper.axis
            grouper = axis[axis.isin(dropped.index)]

        else:

            # create a grouper with the original parameters, but on the dropped
            # object
            grouper, _, _ = _get_grouper(dropped, key=self.keys,
                                         axis=self.axis, level=self.level,
                                         sort=self.sort,
                                         mutated=self.mutated)

        grb = dropped.groupby(grouper, as_index=self.as_index, sort=self.sort)
        sizes, result = grb.size(), grb.nth(n)
        mask = (sizes < max_len).values

        # set the results which don't meet the criteria
        if len(result) and mask.any():
            result.loc[mask] = np.nan

        # reset/reindex to the original groups
        if len(self.obj) == len(dropped) or \
           len(result) == len(self.grouper.result_index):
            result.index = self.grouper.result_index
        else:
            result = result.reindex(self.grouper.result_index)

        return result
