    @Substitution(
        see_also=_agg_see_also_doc,
        examples=_agg_examples_doc,
        versionadded="",
        klass="Series",
        axis="",
    )
    @Appender(_shared_docs["aggregate"])
    def aggregate(self, func=None, *args, **kwargs):

        relabeling = func is None
        columns = None
        no_arg_message = "Must provide 'func' or named aggregation **kwargs."
        if relabeling:
            columns = list(kwargs)
            func = [kwargs[col] for col in columns]
            kwargs = {}
            if not columns:
                raise TypeError(no_arg_message)

        if isinstance(func, str):
            return getattr(self, func)(*args, **kwargs)

        elif isinstance(func, abc.Iterable):
            # Catch instances of lists / tuples
            # but not the class list / tuple itself.
            func = _maybe_mangle_lambdas(func)
            ret = self._aggregate_multiple_funcs(func)
            if relabeling:
                ret.columns = columns
        else:
            cyfunc = self._get_cython_func(func)
            if cyfunc and not args and not kwargs:
                return getattr(self, cyfunc)()

            if self.grouper.nkeys > 1:
                return self._python_agg_general(func, *args, **kwargs)

            try:
                return self._python_agg_general(func, *args, **kwargs)
            except (ValueError, KeyError):
                # TODO: KeyError is raised in _python_agg_general,
                #  see see test_groupby.test_basic
                result = self._aggregate_named(func, *args, **kwargs)

            index = Index(sorted(result), name=self.grouper.names[0])
            ret = create_series_with_explicit_dtype(
                result, index=index, dtype_if_empty=object
            )

        if not self.as_index:  # pragma: no cover
            print("Warning, ignoring as_index=True")

        if isinstance(ret, dict):
            from pandas import concat

            ret = concat(ret, axis=1)
        return ret
