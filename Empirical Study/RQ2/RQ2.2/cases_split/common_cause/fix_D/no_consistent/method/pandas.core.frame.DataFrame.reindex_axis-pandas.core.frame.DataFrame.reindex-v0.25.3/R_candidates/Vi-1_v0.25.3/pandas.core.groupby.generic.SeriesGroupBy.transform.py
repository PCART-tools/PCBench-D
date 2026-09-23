    @Substitution(klass="Series", selected="A.")
    @Appender(_transform_template)
    def transform(self, func, *args, **kwargs):
        func = self._is_cython_func(func) or func

        # if string function
        if isinstance(func, str):
            if func in base.cython_transforms:
                # cythonized transform
                return getattr(self, func)(*args, **kwargs)
            else:
                # cythonized aggregation and merge
                return self._transform_fast(
                    lambda: getattr(self, func)(*args, **kwargs), func
                )

        # reg transform
        klass = self._selected_obj.__class__
        results = []
        wrapper = lambda x: func(x, *args, **kwargs)
        for name, group in self:
            object.__setattr__(group, "name", name)
            res = wrapper(group)

            if isinstance(res, (ABCDataFrame, ABCSeries)):
                res = res._values

            indexer = self._get_index(name)
            s = klass(res, indexer)
            results.append(s)

        # check for empty "results" to avoid concat ValueError
        if results:
            from pandas.core.reshape.concat import concat

            result = concat(results).sort_index()
        else:
            result = Series()

        # we will only try to coerce the result type if
        # we have a numeric dtype, as these are *always* udfs
        # the cython take a different path (and casting)
        dtype = self._selected_obj.dtype
        if is_numeric_dtype(dtype):
            result = maybe_downcast_to_dtype(result, dtype)

        result.name = self._selected_obj.name
        result.index = self._selected_obj.index
        return result
