    def rename_categories(self, new_categories, inplace=False):
        """ Renames categories.

        The new categories has to be a list-like object. All items must be
        unique and the number of items in the new categories must be the same
        as the number of items in the old categories.

        Raises
        ------
        ValueError
            If the new categories do not have the same number of items than the
            current categories or do not validate as categories

        Parameters
        ----------
        new_categories : Index-like
           The renamed categories.
        inplace : boolean (default: False)
           Whether or not to rename the categories inplace or return a copy of
           this categorical with renamed categories.

        Returns
        -------
        cat : Categorical with renamed categories added or None if inplace.

        See also
        --------
        reorder_categories
        add_categories
        remove_categories
        remove_unused_categories
        set_categories
        """
        cat = self if inplace else self.copy()
        cat.categories = new_categories
        if not inplace:
            return cat
