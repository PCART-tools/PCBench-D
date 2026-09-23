    @doc(_agg_template, examples=_agg_examples_doc, klass="Series")
    def aggregate(self, func=None, *args, engine=None, engine_kwargs=None, **kwargs):

        if maybe_use_numba(engine):
            with self._group_selection_context():
                data = self._selected_obj
            result = self._aggregate_with_numba(
                data.to_frame(), func, *args, engine_kwargs=engine_kwargs, **kwargs
            )
            index = self.grouper.result_index
            return self.obj._constructor(result.ravel(), index=index, name=data.name)

        relabeling = func is None
        columns = None
        if relabeling:
            columns, func = validate_func_kwargs(kwargs)
            kwargs = {}

        if isinstance(func, str):
            return getattr(self, func)(*args, **kwargs)

        elif isinstance(func, abc.Iterable):
            # Catch instances of lists / tuples
            # but not the class list / tuple itself.
            func = maybe_mangle_lambdas(func)
            ret = self._aggregate_multiple_funcs(func)
            if relabeling:
                # error: Incompatible types in assignment (expression has type
                # "Optional[List[str]]", variable has type "Index")
                ret.columns = columns  # type: ignore[assignment]
            return ret

        else:
            cyfunc = com.get_cython_func(func)
            if cyfunc and not args and not kwargs:
                return getattr(self, cyfunc)()

            if self.grouper.nkeys > 1:
                return self._python_agg_general(func, *args, **kwargs)

            try:
                return self._python_agg_general(func, *args, **kwargs)
            except KeyError:
                # TODO: KeyError is raised in _python_agg_general,
                #  see test_groupby.test_basic
                result = self._aggregate_named(func, *args, **kwargs)

                # result is a dict whose keys are the elements of result_index
                index = self.grouper.result_index
                return create_series_with_explicit_dtype(
                    result, index=index, dtype_if_empty=object
                )
