    @Substitution(klass='DataFrame', selected='')
    @Appender(_transform_template)
    def transform(self, func, *args, **kwargs):

        # optimized transforms
        func = self._is_cython_func(func) or func
        if isinstance(func, compat.string_types):
            if func in _cython_transforms:
                # cythonized transform
                return getattr(self, func)(*args, **kwargs)
            else:
                # cythonized aggregation and merge
                result = getattr(self, func)(*args, **kwargs)
        else:
            return self._transform_general(func, *args, **kwargs)

        # a reduction transform
        if not isinstance(result, DataFrame):
            return self._transform_general(func, *args, **kwargs)

        obj = self._obj_with_exclusions
        # nuiscance columns
        if not result.columns.equals(obj.columns):
            return self._transform_general(func, *args, **kwargs)

        return self._transform_fast(result, obj)
