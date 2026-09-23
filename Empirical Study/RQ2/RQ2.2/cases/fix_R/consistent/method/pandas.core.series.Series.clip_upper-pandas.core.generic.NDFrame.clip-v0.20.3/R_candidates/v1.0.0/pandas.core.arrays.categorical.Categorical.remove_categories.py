    def remove_categories(self, removals, inplace=False):
        """
        Remove the specified categories.

        `removals` must be included in the old categories. Values which were in
        the removed categories will be set to NaN

        Parameters
        ----------
        removals : category or list of categories
           The categories which should be removed.
        inplace : bool, default False
           Whether or not to remove the categories inplace or return a copy of
           this categorical with removed categories.

        Returns
        -------
        cat : Categorical with removed categories or None if inplace.

        Raises
        ------
        ValueError
            If the removals are not contained in the categories

        See Also
        --------
        rename_categories
        reorder_categories
        add_categories
        remove_unused_categories
        set_categories
        """
        inplace = validate_bool_kwarg(inplace, "inplace")
        if not is_list_like(removals):
            removals = [removals]

        removal_set = set(removals)
        not_included = removal_set - set(self.dtype.categories)
        new_categories = [c for c in self.dtype.categories if c not in removal_set]

        # GH 10156
        if any(isna(removals)):
            not_included = {x for x in not_included if notna(x)}
            new_categories = [x for x in new_categories if notna(x)]

        if len(not_included) != 0:
            raise ValueError(f"removals must all be in old categories: {not_included}")

        return self.set_categories(
            new_categories, ordered=self.ordered, rename=False, inplace=inplace
        )
