    def map(
        self,
        mapper,
        na_action: Literal["ignore"] | None | lib.NoDefault = lib.no_default,
    ):
        """
        Map categories using an input mapping or function.

        Maps the categories to new categories. If the mapping correspondence is
        one-to-one the result is a :class:`~pandas.Categorical` which has the
        same order property as the original, otherwise a :class:`~pandas.Index`
        is returned. NaN values are unaffected.

        If a `dict` or :class:`~pandas.Series` is used any unmapped category is
        mapped to `NaN`. Note that if this happens an :class:`~pandas.Index`
        will be returned.

        Parameters
        ----------
        mapper : function, dict, or Series
            Mapping correspondence.
        na_action : {None, 'ignore'}, default 'ignore'
            If 'ignore', propagate NaN values, without passing them to the
            mapping correspondence.

            .. deprecated:: 2.1.0

               The default value of 'ignore' has been deprecated and will be changed to
               None in the future.

        Returns
        -------
        pandas.Categorical or pandas.Index
            Mapped categorical.

        See Also
        --------
        CategoricalIndex.map : Apply a mapping correspondence on a
            :class:`~pandas.CategoricalIndex`.
        Index.map : Apply a mapping correspondence on an
            :class:`~pandas.Index`.
        Series.map : Apply a mapping correspondence on a
            :class:`~pandas.Series`.
        Series.apply : Apply more complex functions on a
            :class:`~pandas.Series`.

        Examples
        --------
        >>> cat = pd.Categorical(['a', 'b', 'c'])
        >>> cat
        ['a', 'b', 'c']
        Categories (3, object): ['a', 'b', 'c']
        >>> cat.map(lambda x: x.upper(), na_action=None)
        ['A', 'B', 'C']
        Categories (3, object): ['A', 'B', 'C']
        >>> cat.map({'a': 'first', 'b': 'second', 'c': 'third'}, na_action=None)
        ['first', 'second', 'third']
        Categories (3, object): ['first', 'second', 'third']

        If the mapping is one-to-one the ordering of the categories is
        preserved:

        >>> cat = pd.Categorical(['a', 'b', 'c'], ordered=True)
        >>> cat
        ['a', 'b', 'c']
        Categories (3, object): ['a' < 'b' < 'c']
        >>> cat.map({'a': 3, 'b': 2, 'c': 1}, na_action=None)
        [3, 2, 1]
        Categories (3, int64): [3 < 2 < 1]

        If the mapping is not one-to-one an :class:`~pandas.Index` is returned:

        >>> cat.map({'a': 'first', 'b': 'second', 'c': 'first'}, na_action=None)
        Index(['first', 'second', 'first'], dtype='object')

        If a `dict` is used, all unmapped categories are mapped to `NaN` and
        the result is an :class:`~pandas.Index`:

        >>> cat.map({'a': 'first', 'b': 'second'}, na_action=None)
        Index(['first', 'second', nan], dtype='object')
        """
        if na_action is lib.no_default:
            warnings.warn(
                "The default value of 'ignore' for the `na_action` parameter in "
                "pandas.Categorical.map is deprecated and will be "
                "changed to 'None' in a future version. Please set na_action to the "
                "desired value to avoid seeing this warning",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            na_action = "ignore"

        assert callable(mapper) or is_dict_like(mapper)

        new_categories = self.categories.map(mapper)

        has_nans = np.any(self._codes == -1)

        na_val = np.nan
        if na_action is None and has_nans:
            na_val = mapper(np.nan) if callable(mapper) else mapper.get(np.nan, np.nan)

        if new_categories.is_unique and not new_categories.hasnans and na_val is np.nan:
            new_dtype = CategoricalDtype(new_categories, ordered=self.ordered)
            return self.from_codes(self._codes.copy(), dtype=new_dtype, validate=False)

        if has_nans:
            new_categories = new_categories.insert(len(new_categories), na_val)

        return np.take(new_categories, self._codes)
