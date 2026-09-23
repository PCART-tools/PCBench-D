    def set_categories(self, new_categories, ordered=None, rename=False,
                       inplace=False):
        """
        Sets the categories to the specified new_categories.

        `new_categories` can include new categories (which will result in
        unused categories) or remove old categories (which results in values
        set to NaN). If `rename==True`, the categories will simple be renamed
        (less or more items than in old categories will result in values set to
        NaN or in unused categories respectively).

        This method can be used to perform more than one action of adding,
        removing, and reordering simultaneously and is therefore faster than
        performing the individual steps via the more specialised methods.

        On the other hand this methods does not do checks (e.g., whether the
        old categories are included in the new categories on a reorder), which
        can result in surprising changes, for example when using special string
        dtypes on python3, which does not considers a S1 string equal to a
        single char python string.

        Parameters
        ----------
        new_categories : Index-like
           The categories in new order.
        ordered : boolean, (default: False)
           Whether or not the categorical is treated as a ordered categorical.
           If not given, do not change the ordered information.
        rename : boolean (default: False)
           Whether or not the new_categories should be considered as a rename
           of the old categories or as reordered categories.
        inplace : boolean (default: False)
           Whether or not to reorder the categories inplace or return a copy of
           this categorical with reordered categories.

        Returns
        -------
        cat : Categorical with reordered categories or None if inplace.

        Raises
        ------
        ValueError
            If new_categories does not validate as categories

        See Also
        --------
        rename_categories
        reorder_categories
        add_categories
        remove_categories
        remove_unused_categories
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        if ordered is None:
            ordered = self.dtype.ordered
        new_dtype = CategoricalDtype(new_categories, ordered=ordered)

        cat = self if inplace else self.copy()
        if rename:
            if (cat.dtype.categories is not None and
                    len(new_dtype.categories) < len(cat.dtype.categories)):
                # remove all _codes which are larger and set to -1/NaN
                cat._codes[cat._codes >= len(new_dtype.categories)] = -1
        else:
            codes = _recode_for_categories(cat.codes, cat.categories,
                                           new_dtype.categories)
            cat._codes = codes
        cat._dtype = new_dtype

        if not inplace:
            return cat
