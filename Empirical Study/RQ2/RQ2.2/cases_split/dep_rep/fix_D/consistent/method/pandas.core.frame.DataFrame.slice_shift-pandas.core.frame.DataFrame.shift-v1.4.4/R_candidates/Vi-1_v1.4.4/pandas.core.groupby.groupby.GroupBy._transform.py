    @final
    def _transform(self, func, *args, engine=None, engine_kwargs=None, **kwargs):

        if maybe_use_numba(engine):
            # TODO: tests with self._selected_obj.ndim == 1 on DataFrameGroupBy
            with self._group_selection_context():
                data = self._selected_obj
            df = data if data.ndim == 2 else data.to_frame()
            result = self._transform_with_numba(
                df, func, *args, engine_kwargs=engine_kwargs, **kwargs
            )
            if self.obj.ndim == 2:
                return cast(DataFrame, self.obj)._constructor(
                    result, index=data.index, columns=data.columns
                )
            else:
                return cast(Series, self.obj)._constructor(
                    result.ravel(), index=data.index, name=data.name
                )

        # optimized transforms
        func = com.get_cython_func(func) or func

        if not isinstance(func, str):
            return self._transform_general(func, *args, **kwargs)

        elif func not in base.transform_kernel_allowlist:
            msg = f"'{func}' is not a valid function name for transform(name)"
            raise ValueError(msg)
        elif func in base.cythonized_kernels or func in base.transformation_kernels:
            # cythonized transform or canned "agg+broadcast"
            return getattr(self, func)(*args, **kwargs)

        else:
            # i.e. func in base.reduction_kernels

            # GH#30918 Use _transform_fast only when we know func is an aggregation
            # If func is a reduction, we need to broadcast the
            # result to the whole group. Compute func result
            # and deal with possible broadcasting below.
            # Temporarily set observed for dealing with categoricals.
            with com.temp_setattr(self, "observed", True):
                result = getattr(self, func)(*args, **kwargs)

            if self._can_use_transform_fast(result):
                return self._wrap_transform_fast_result(result)

            # only reached for DataFrameGroupBy
            return self._transform_general(func, *args, **kwargs)
