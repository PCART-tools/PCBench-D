    @Substitution(klass="DataFrame", selected="")
    @Appender(_transform_template)
    def transform(self, func, *args, **kwargs):

        # optimized transforms
        func = self._get_cython_func(func) or func

        if not isinstance(func, str):
            return self._transform_general(func, *args, **kwargs)

        elif func not in base.transform_kernel_whitelist:
            msg = f"'{func}' is not a valid function name for transform(name)"
            raise ValueError(msg)
        elif func in base.cythonized_kernels:
            # cythonized transformation or canned "reduction+broadcast"
            return getattr(self, func)(*args, **kwargs)

        # If func is a reduction, we need to broadcast the
        # result to the whole group. Compute func result
        # and deal with possible broadcasting below.
        result = getattr(self, func)(*args, **kwargs)

        # a reduction transform
        if not isinstance(result, DataFrame):
            return self._transform_general(func, *args, **kwargs)

        obj = self._obj_with_exclusions

        # nuisance columns
        if not result.columns.equals(obj.columns):
            return self._transform_general(func, *args, **kwargs)

        return self._transform_fast(result, func)
