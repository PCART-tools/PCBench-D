    def _concat(self, to_concat: list[Index], name: Hashable) -> Index:
        # if calling index is category, don't check dtype of others
        try:
            codes = np.concatenate([self._is_dtype_compat(c).codes for c in to_concat])
        except TypeError:
            # not all to_concat elements are among our categories (or NA)
            from pandas.core.dtypes.concat import concat_compat

            res = concat_compat(to_concat)
            return Index(res, name=name)
        else:
            cat = self._data._from_backing_data(codes)
            return type(self)._simple_new(cat, name=name)
