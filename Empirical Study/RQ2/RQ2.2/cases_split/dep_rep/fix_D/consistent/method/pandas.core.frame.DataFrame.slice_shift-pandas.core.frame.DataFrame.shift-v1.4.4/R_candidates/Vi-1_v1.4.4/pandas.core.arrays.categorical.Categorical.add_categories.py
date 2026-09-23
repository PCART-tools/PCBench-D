    def add_categories(self, new_categories, inplace=no_default):
        """
        Add new categories.

        `new_categories` will be included at the last/highest place in the
        categories and will be unused directly after this call.

        Parameters
        ----------
        new_categories : category or list-like of category
           The new categories to be included.
        inplace : bool, default False
           Whether or not to add the categories inplace or return a copy of
           this categorical with added categories.

           .. deprecated:: 1.3.0

        Returns
        -------
        cat : Categorical or None
            Categorical with new categories added or None if ``inplace=True``.

        Raises
        ------
        ValueError
            If the new categories include old categories or do not validate as
            categories

        See Also
        --------
        rename_categories : Rename categories.
        reorder_categories : Reorder categories.
        remove_categories : Remove the specified categories.
        remove_unused_categories : Remove categories which are not used.
        set_categories : Set the categories to the specified ones.

        Examples
        --------
        >>> c = pd.Categorical(['c', 'b', 'c'])
        >>> c
        ['c', 'b', 'c']
        Categories (2, object): ['b', 'c']

        >>> c.add_categories(['d', 'a'])
        ['c', 'b', 'c']
        Categories (4, object): ['b', 'c', 'd', 'a']
        """
        if inplace is not no_default:
            warn(
                "The `inplace` parameter in pandas.Categorical."
                "add_categories is deprecated and will be removed in "
                "a future version. Removing unused categories will always "
                "return a new Categorical object.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        else:
            inplace = False

        inplace = validate_bool_kwarg(inplace, "inplace")
        if not is_list_like(new_categories):
            new_categories = [new_categories]
        already_included = set(new_categories) & set(self.dtype.categories)
        if len(already_included) != 0:
            raise ValueError(
                f"new categories must not include old categories: {already_included}"
            )
        new_categories = list(self.dtype.categories) + list(new_categories)
        new_dtype = CategoricalDtype(new_categories, self.ordered)

        cat = self if inplace else self.copy()
        codes = coerce_indexer_dtype(cat._ndarray, new_dtype.categories)
        NDArrayBacked.__init__(cat, codes, new_dtype)
        if not inplace:
            return cat
