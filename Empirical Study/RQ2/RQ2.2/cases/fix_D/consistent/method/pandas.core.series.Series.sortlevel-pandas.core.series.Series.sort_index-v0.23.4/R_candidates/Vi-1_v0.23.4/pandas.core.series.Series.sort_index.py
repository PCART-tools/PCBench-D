    def sort_index(self, axis=0, level=None, ascending=True, inplace=False,
                   kind='quicksort', na_position='last', sort_remaining=True):
        """
        Sort Series by index labels.

        Returns a new Series sorted by label if `inplace` argument is
        ``False``, otherwise updates the original series and returns None.

        Parameters
        ----------
        axis : int, default 0
            Axis to direct sorting. This can only be 0 for Series.
        level : int, optional
            If not None, sort on values in specified index level(s).
        ascending : bool, default true
            Sort ascending vs. descending.
        inplace : bool, default False
            If True, perform operation in-place.
        kind : {'quicksort', 'mergesort', 'heapsort'}, default 'quicksort'
            Choice of sorting algorithm. See also :func:`numpy.sort` for more
            information.  'mergesort' is the only stable algorithm. For
            DataFrames, this option is only applied when sorting on a single
            column or label.
        na_position : {'first', 'last'}, default 'last'
            If 'first' puts NaNs at the beginning, 'last' puts NaNs at the end.
            Not implemented for MultiIndex.
        sort_remaining : bool, default True
            If true and sorting by level and index is multilevel, sort by other
            levels too (in order) after sorting by specified level.

        Returns
        -------
        pandas.Series
            The original Series sorted by the labels

        See Also
        --------
        DataFrame.sort_index: Sort DataFrame by the index
        DataFrame.sort_values: Sort DataFrame by the value
        Series.sort_values : Sort Series by the value

        Examples
        --------
        >>> s = pd.Series(['a', 'b', 'c', 'd'], index=[3, 2, 1, 4])
        >>> s.sort_index()
        1    c
        2    b
        3    a
        4    d
        dtype: object

        Sort Descending

        >>> s.sort_index(ascending=False)
        4    d
        3    a
        2    b
        1    c
        dtype: object

        Sort Inplace

        >>> s.sort_index(inplace=True)
        >>> s
        1    c
        2    b
        3    a
        4    d
        dtype: object

        By default NaNs are put at the end, but use `na_position` to place
        them at the beginning

        >>> s = pd.Series(['a', 'b', 'c', 'd'], index=[3, 2, 1, np.nan])
        >>> s.sort_index(na_position='first')
        NaN     d
         1.0    c
         2.0    b
         3.0    a
        dtype: object

        Specify index level to sort

        >>> arrays = [np.array(['qux', 'qux', 'foo', 'foo',
        ...                     'baz', 'baz', 'bar', 'bar']),
        ...           np.array(['two', 'one', 'two', 'one',
        ...                     'two', 'one', 'two', 'one'])]
        >>> s = pd.Series([1, 2, 3, 4, 5, 6, 7, 8], index=arrays)
        >>> s.sort_index(level=1)
        bar  one    8
        baz  one    6
        foo  one    4
        qux  one    2
        bar  two    7
        baz  two    5
        foo  two    3
        qux  two    1
        dtype: int64

        Does not sort by remaining levels when sorting by levels

        >>> s.sort_index(level=1, sort_remaining=False)
        qux  one    2
        foo  one    4
        baz  one    6
        bar  one    8
        qux  two    1
        foo  two    3
        baz  two    5
        bar  two    7
        dtype: int64
        """
        # TODO: this can be combined with DataFrame.sort_index impl as
        # almost identical
        inplace = validate_bool_kwarg(inplace, 'inplace')
        axis = self._get_axis_number(axis)
        index = self.index

        if level is not None:
            new_index, indexer = index.sortlevel(level, ascending=ascending,
                                                 sort_remaining=sort_remaining)
        elif isinstance(index, MultiIndex):
            from pandas.core.sorting import lexsort_indexer
            labels = index._sort_levels_monotonic()
            indexer = lexsort_indexer(labels._get_labels_for_sorting(),
                                      orders=ascending,
                                      na_position=na_position)
        else:
            from pandas.core.sorting import nargsort

            # Check monotonic-ness before sort an index
            # GH11080
            if ((ascending and index.is_monotonic_increasing) or
                    (not ascending and index.is_monotonic_decreasing)):
                if inplace:
                    return
                else:
                    return self.copy()

            indexer = nargsort(index, kind=kind, ascending=ascending,
                               na_position=na_position)

        indexer = _ensure_platform_int(indexer)
        new_index = index.take(indexer)
        new_index = new_index._sort_levels_monotonic()

        new_values = self._values.take(indexer)
        result = self._constructor(new_values, index=new_index)

        if inplace:
            self._update_inplace(result)
        else:
            return result.__finalize__(self)
