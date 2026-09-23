    def remove_unused_categories(self, inplace=False):
        """
        Removes categories which are not used.

        Parameters
        ----------
        inplace : boolean (default: False)
           Whether or not to drop unused categories inplace or return a copy of
           this categorical with unused categories dropped.

        Returns
        -------
        cat : Categorical with unused categories dropped or None if inplace.

        See Also
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

        new_categories = cat.dtype.categories.take(idx)
        new_dtype = CategoricalDtype._from_fastpath(new_categories,
                                                    ordered=self.ordered)
        cat._dtype = new_dtype
        cat._codes = coerce_indexer_dtype(inv, new_dtype.categories)

        if not inplace:
            return cat
