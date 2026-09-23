    @final
    def _transform(self, func, *args, engine=None, engine_kwargs=None, **kwargs):
        # optimized transforms
        orig_func = func
        func = com.get_cython_func(func) or func
        if orig_func != func:
            warn_alias_replacement(self, orig_func, func)

        if not isinstance(func, str):
            return self._transform_general(func, engine, engine_kwargs, *args, **kwargs)

        elif func not in base.transform_kernel_allowlist:
            msg = f"'{func}' is not a valid function name for transform(name)"
            raise ValueError(msg)
        elif func in base.cythonized_kernels or func in base.transformation_kernels:
            # cythonized transform or canned "agg+broadcast"
            if engine is not None:
                kwargs["engine"] = engine
                kwargs["engine_kwargs"] = engine_kwargs
            return getattr(self, func)(*args, **kwargs)

        else:
            # i.e. func in base.reduction_kernels

            # GH#30918 Use _transform_fast only when we know func is an aggregation
            # If func is a reduction, we need to broadcast the
            # result to the whole group. Compute func result
            # and deal with possible broadcasting below.
            # Temporarily set observed for dealing with categoricals.
            with com.temp_setattr(self, "observed", True):
                with com.temp_setattr(self, "as_index", True):
                    # GH#49834 - result needs groups in the index for
                    # _wrap_transform_fast_result
                    if engine is not None:
                        kwargs["engine"] = engine
                        kwargs["engine_kwargs"] = engine_kwargs
                    result = getattr(self, func)(*args, **kwargs)

            return self._wrap_transform_fast_result(result)
