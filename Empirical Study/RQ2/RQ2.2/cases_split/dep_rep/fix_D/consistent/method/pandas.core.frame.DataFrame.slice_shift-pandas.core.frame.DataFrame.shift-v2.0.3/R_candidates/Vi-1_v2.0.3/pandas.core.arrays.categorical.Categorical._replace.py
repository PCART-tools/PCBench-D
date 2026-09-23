    def _replace(self, *, to_replace, value, inplace: bool = False):
        from pandas import Index

        inplace = validate_bool_kwarg(inplace, "inplace")
        cat = self if inplace else self.copy()

        mask = isna(np.asarray(value))
        if mask.any():
            removals = np.asarray(to_replace)[mask]
            removals = cat.categories[cat.categories.isin(removals)]
            new_cat = cat.remove_categories(removals)
            NDArrayBacked.__init__(cat, new_cat.codes, new_cat.dtype)

        ser = cat.categories.to_series()
        ser = ser.replace(to_replace=to_replace, value=value)

        all_values = Index(ser)

        # GH51016: maintain order of existing categories
        idxr = cat.categories.get_indexer_for(all_values)
        locs = np.arange(len(ser))
        locs = np.where(idxr == -1, locs, idxr)
        locs = locs.argsort()

        new_categories = ser.take(locs)
        new_categories = new_categories.drop_duplicates(keep="first")
        new_categories = Index(new_categories)
        new_codes = recode_for_categories(
            cat._codes, all_values, new_categories, copy=False
        )
        new_dtype = CategoricalDtype(new_categories, ordered=self.dtype.ordered)
        NDArrayBacked.__init__(cat, new_codes, new_dtype)

        if not inplace:
            return cat
