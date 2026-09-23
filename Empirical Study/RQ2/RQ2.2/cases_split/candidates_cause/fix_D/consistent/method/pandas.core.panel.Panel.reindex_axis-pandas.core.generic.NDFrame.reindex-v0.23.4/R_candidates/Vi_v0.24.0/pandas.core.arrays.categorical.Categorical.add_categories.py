    def add_categories(self, new_categories, inplace=False):
        """
        Add new categories.

        `new_categories` will be included at the last/highest place in the
        categories and will be unused directly after this call.

        Parameters
        ----------
        new_categories : category or list-like of category
           The new categories to be included.
        inplace : boolean (default: False)
           Whether or not to add the categories inplace or return a copy of
           this categorical with added categories.

        Returns
        -------
        cat : Categorical with new categories added or None if inplace.

        Raises
        ------
        ValueError
            If the new categories include old categories or do not validate as
            categories

        See Also
        --------
        rename_categories
        reorder_categories
        remove_categories
        remove_unused_categories
        set_categories
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        if not is_list_like(new_categories):
            new_categories = [new_categories]
        already_included = set(new_categories) & set(self.dtype.categories)
        if len(already_included) != 0:
            msg = ("new categories must not include old categories: "
                   "{already_included!s}")
            raise ValueError(msg.format(already_included=already_included))
        new_categories = list(self.dtype.categories) + list(new_categories)
        new_dtype = CategoricalDtype(new_categories, self.ordered)

        cat = self if inplace else self.copy()
        cat._dtype = new_dtype
        cat._codes = coerce_indexer_dtype(cat._codes, new_dtype.categories)
        if not inplace:
            return cat
