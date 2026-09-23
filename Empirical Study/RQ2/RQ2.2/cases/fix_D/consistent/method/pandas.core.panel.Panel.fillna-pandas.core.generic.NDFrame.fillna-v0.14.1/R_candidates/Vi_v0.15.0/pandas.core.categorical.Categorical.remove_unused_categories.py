    def remove_unused_categories(self, inplace=False):
        """ Removes categories which are not used.

        Parameters
        ----------
        inplace : boolean (default: False)
           Whether or not to drop unused categories inplace or return a copy of this categorical
           with unused categories dropped.

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
        cat = self if inplace else self.copy()
        _used = sorted(np.unique(cat._codes))
        new_categories = cat.categories.take(com._ensure_platform_int(_used))
        new_categories = _ensure_index(new_categories)
        cat._codes = _get_codes_for_values(cat.__array__(), new_categories)
        cat._categories = new_categories
        if not inplace:
            return cat
