    def remove_unused_categories(self, inplace=False):
        """ Removes categories which are not used.

        Parameters
        ----------
        inplace : boolean (default: False)
           Whether or not to drop unused categories inplace or return a copy of
           this categorical with unused categories dropped.

        Returns
        -------
        cat : Categorical with unused categories dropped or None if inplace.

        See also
        --------
        rename_categories
        reorder_categories
        add_categories
        remove_categories
        set_categories
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        cat = self if inplace else self.copy()
        idx, inv = np.unique(cat._codes, return_inverse=True)

        if idx.size != 0 and idx[0] == -1:  # na sentinel
            idx, inv = idx[1:], inv - 1

        cat._categories = cat.categories.take(idx)
        cat._codes = coerce_indexer_dtype(inv, self._categories)

        if not inplace:
            return cat
