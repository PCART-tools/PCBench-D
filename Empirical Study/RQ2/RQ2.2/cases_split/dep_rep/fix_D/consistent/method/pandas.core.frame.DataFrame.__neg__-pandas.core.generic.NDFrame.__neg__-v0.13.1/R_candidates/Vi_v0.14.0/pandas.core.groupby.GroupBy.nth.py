    def nth(self, n, dropna=None):
        """
        Take the nth row from each group.

        If dropna, will not show nth non-null row, dropna is either
        Truthy (if a Series) or 'all', 'any' (if a DataFrame); this is equivalent
        to calling dropna(how=dropna) before the groupby.

        Examples
        --------
        >>> DataFrame([[1, np.nan], [1, 4], [5, 6]], columns=['A', 'B'])
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

        self._set_selection_from_grouper()
        if not dropna:  # good choice
            m = self.grouper._max_groupsize
            if n >= m or n < -m:
                return self._selected_obj.loc[[]]
            rng = np.zeros(m, dtype=bool)
            if n >= 0:
                rng[n] = True
                is_nth = self._cumcount_array(rng)
            else:
                rng[- n - 1] = True
                is_nth = self._cumcount_array(rng, ascending=False)

            result = self._selected_obj[is_nth]

            # the result index
            if self.as_index:
                ax = self.obj._info_axis
                names = self.grouper.names
                if all([ n in ax for n in names ]):
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

        max_len = n if n >= 0 else - 1 - n

        def picker(x):
            x = x.dropna(how=dropna)  # Note: how is ignored if Series
            if len(x) <= max_len:
                return np.nan
            else:
                return x.iloc[n]

        return self.agg(picker)
