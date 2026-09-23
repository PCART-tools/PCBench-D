    def sort_values(self, inplace=False, ascending=True, na_position='last'):
        """ Sorts the Categorical by category value returning a new
        Categorical by default.

        While an ordering is applied to the category values, sorting in this
        context refers more to organizing and grouping together based on
        matching category values. Thus, this function can be called on an
        unordered Categorical instance unlike the functions 'Categorical.min'
        and 'Categorical.max'.

        Parameters
        ----------
        inplace : boolean, default False
            Do operation in place.
        ascending : boolean, default True
            Order ascending. Passing False orders descending. The
            ordering parameter provides the method by which the
            category values are organized.
        na_position : {'first', 'last'} (optional, default='last')
            'first' puts NaNs at the beginning
            'last' puts NaNs at the end

        Returns
        -------
        y : Categorical or None

        See Also
        --------
        Categorical.sort
        Series.sort_values

        Examples
        --------
        >>> c = pd.Categorical([1, 2, 2, 1, 5])
        >>> c
        [1, 2, 2, 1, 5]
        Categories (3, int64): [1, 2, 5]
        >>> c.sort_values()
        [1, 1, 2, 2, 5]
        Categories (3, int64): [1, 2, 5]
        >>> c.sort_values(ascending=False)
        [5, 2, 2, 1, 1]
        Categories (3, int64): [1, 2, 5]

        Inplace sorting can be done as well:

        >>> c.sort_values(inplace=True)
        >>> c
        [1, 1, 2, 2, 5]
        Categories (3, int64): [1, 2, 5]
        >>>
        >>> c = pd.Categorical([1, 2, 2, 1, 5])

        'sort_values' behaviour with NaNs. Note that 'na_position'
        is independent of the 'ascending' parameter:

        >>> c = pd.Categorical([np.nan, 2, 2, np.nan, 5])
        >>> c
        [NaN, 2.0, 2.0, NaN, 5.0]
        Categories (2, int64): [2, 5]
        >>> c.sort_values()
        [2.0, 2.0, 5.0, NaN, NaN]
        Categories (2, int64): [2, 5]
        >>> c.sort_values(ascending=False)
        [5.0, 2.0, 2.0, NaN, NaN]
        Categories (2, int64): [2, 5]
        >>> c.sort_values(na_position='first')
        [NaN, NaN, 2.0, 2.0, 5.0]
        Categories (2, int64): [2, 5]
        >>> c.sort_values(ascending=False, na_position='first')
        [NaN, NaN, 5.0, 2.0, 2.0]
        Categories (2, int64): [2, 5]
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        if na_position not in ['last', 'first']:
            raise ValueError('invalid na_position: {!r}'.format(na_position))

        codes = np.sort(self._codes)
        if not ascending:
            codes = codes[::-1]

        # NaN handling
        na_mask = (codes == -1)
        if na_mask.any():
            n_nans = len(codes[na_mask])
            if na_position == "first":
                # in this case sort to the front
                new_codes = codes.copy()
                new_codes[0:n_nans] = -1
                new_codes[n_nans:] = codes[~na_mask]
                codes = new_codes
            elif na_position == "last":
                # ... and to the end
                new_codes = codes.copy()
                pos = len(codes) - n_nans
                new_codes[0:pos] = codes[~na_mask]
                new_codes[pos:] = -1
                codes = new_codes
        if inplace:
            self._codes = codes
            return
        else:
            return self._constructor(values=codes, categories=self.categories,
                                     ordered=self.ordered, fastpath=True)
