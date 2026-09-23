    def _transform_general(self, func, *args, **kwargs):
        """
        Transform with a non-str `func`.
        """
        klass = type(self._selected_obj)

        results = []
        for name, group in self:
            object.__setattr__(group, "name", name)
            res = func(group, *args, **kwargs)

            if isinstance(res, (ABCDataFrame, ABCSeries)):
                res = res._values

            indexer = self._get_index(name)
            ser = klass(res, indexer)
            results.append(ser)

        # check for empty "results" to avoid concat ValueError
        if results:
            from pandas.core.reshape.concat import concat

            result = concat(results).sort_index()
        else:
            result = Series(dtype=np.float64)

        # we will only try to coerce the result type if
        # we have a numeric dtype, as these are *always* user-defined funcs
        # the cython take a different path (and casting)
        dtype = self._selected_obj.dtype
        if is_numeric_dtype(dtype):
            result = maybe_downcast_to_dtype(result, dtype)

        result.name = self._selected_obj.name
        result.index = self._selected_obj.index
        return result
