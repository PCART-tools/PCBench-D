    def remove_unused_categories(self, inplace=no_default):
        """
        Remove categories which are not used.

        Parameters
        ----------
        inplace : bool, default False
           Whether or not to drop unused categories inplace or return a copy of
           this categorical with unused categories dropped.

           .. deprecated:: 1.2.0

        Returns
        -------
        cat : Categorical or None
            Categorical with unused categories dropped or None if ``inplace=True``.

        See Also
        --------
        rename_categories : Rename categories.
        reorder_categories : Reorder categories.
        add_categories : Add new categories.
        remove_categories : Remove the specified categories.
        set_categories : Set the categories to the specified ones.

        Examples
        --------
        >>> c = pd.Categorical(['a', 'c', 'b', 'c', 'd'])
        >>> c
        ['a', 'c', 'b', 'c', 'd']
        Categories (4, object): ['a', 'b', 'c', 'd']

        >>> c[2] = 'a'
        >>> c[4] = 'c'
        >>> c
        ['a', 'c', 'a', 'c', 'c']
        Categories (4, object): ['a', 'b', 'c', 'd']

        >>> c.remove_unused_categories()
        ['a', 'c', 'a', 'c', 'c']
        Categories (2, object): ['a', 'c']
        """
        if inplace is not no_default:
            warn(
                "The `inplace` parameter in pandas.Categorical."
                "remove_unused_categories is deprecated and "
                "will be removed in a future version.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        else:
            inplace = False

        inplace = validate_bool_kwarg(inplace, "inplace")
        cat = self if inplace else self.copy()
        idx, inv = np.unique(cat._codes, return_inverse=True)

        if idx.size != 0 and idx[0] == -1:  # na sentinel
            idx, inv = idx[1:], inv - 1

        new_categories = cat.dtype.categories.take(idx)
        new_dtype = CategoricalDtype._from_fastpath(
            new_categories, ordered=self.ordered
        )
        new_codes = coerce_indexer_dtype(inv, new_dtype.categories)
        NDArrayBacked.__init__(cat, new_codes, new_dtype)
        if not inplace:
            return cat
