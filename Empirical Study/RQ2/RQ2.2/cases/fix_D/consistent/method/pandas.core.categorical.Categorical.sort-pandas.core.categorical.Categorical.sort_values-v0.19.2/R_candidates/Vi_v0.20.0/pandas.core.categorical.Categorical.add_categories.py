    def add_categories(self, new_categories, inplace=False):
        """ Add new categories.

        `new_categories` will be included at the last/highest place in the
        categories and will be unused directly after this call.

        Raises
        ------
        ValueError
            If the new categories include old categories or do not validate as
            categories

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

        See also
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
        already_included = set(new_categories) & set(self._categories)
        if len(already_included) != 0:
            msg = ("new categories must not include old categories: %s" %
                   str(already_included))
            raise ValueError(msg)
        new_categories = list(self._categories) + list(new_categories)
        cat = self if inplace else self.copy()
        cat._categories = self._validate_categories(new_categories)
        cat._codes = coerce_indexer_dtype(cat._codes, new_categories)
        if not inplace:
            return cat
