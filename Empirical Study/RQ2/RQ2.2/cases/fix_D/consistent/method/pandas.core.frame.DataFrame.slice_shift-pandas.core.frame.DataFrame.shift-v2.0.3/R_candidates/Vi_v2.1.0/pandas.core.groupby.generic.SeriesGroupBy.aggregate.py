    @doc(_agg_template_series, examples=_agg_examples_doc, klass="Series")
    def aggregate(self, func=None, *args, engine=None, engine_kwargs=None, **kwargs):
        relabeling = func is None
        columns = None
        if relabeling:
            columns, func = validate_func_kwargs(kwargs)
            kwargs = {}

        if isinstance(func, str):
            if maybe_use_numba(engine):
                # Not all agg functions support numba, only propagate numba kwargs
                # if user asks for numba
                kwargs["engine"] = engine
                kwargs["engine_kwargs"] = engine_kwargs
            return getattr(self, func)(*args, **kwargs)

        elif isinstance(func, abc.Iterable):
            # Catch instances of lists / tuples
            # but not the class list / tuple itself.
            func = maybe_mangle_lambdas(func)
            kwargs["engine"] = engine
            kwargs["engine_kwargs"] = engine_kwargs
            ret = self._aggregate_multiple_funcs(func, *args, **kwargs)
            if relabeling:
                # columns is not narrowed by mypy from relabeling flag
                assert columns is not None  # for mypy
                ret.columns = columns
            if not self.as_index:
                ret = ret.reset_index()
            return ret

        else:
            cyfunc = com.get_cython_func(func)
            if cyfunc and not args and not kwargs:
                warn_alias_replacement(self, func, cyfunc)
                return getattr(self, cyfunc)()

            if maybe_use_numba(engine):
                return self._aggregate_with_numba(
                    func, *args, engine_kwargs=engine_kwargs, **kwargs
                )

            if self.ngroups == 0:
                # e.g. test_evaluate_with_empty_groups without any groups to
                #  iterate over, we have no output on which to do dtype
                #  inference. We default to using the existing dtype.
                #  xref GH#51445
                obj = self._obj_with_exclusions
                return self.obj._constructor(
                    [],
                    name=self.obj.name,
                    index=self.grouper.result_index,
                    dtype=obj.dtype,
                )

            if self.grouper.nkeys > 1:
                return self._python_agg_general(func, *args, **kwargs)

            try:
                return self._python_agg_general(func, *args, **kwargs)
            except KeyError:
                # KeyError raised in test_groupby.test_basic is bc the func does
                #  a dictionary lookup on group.name, but group name is not
                #  pinned in _python_agg_general, only in _aggregate_named
                result = self._aggregate_named(func, *args, **kwargs)

                warnings.warn(
                    "Pinning the groupby key to each group in "
                    f"{type(self).__name__}.agg is deprecated, and cases that "
                    "relied on it will raise in a future version. "
                    "If your operation requires utilizing the groupby keys, "
                    "iterate over the groupby object instead.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )

                # result is a dict whose keys are the elements of result_index
                result = Series(result, index=self.grouper.result_index)
                result = self._wrap_aggregated_output(result)
                return result
