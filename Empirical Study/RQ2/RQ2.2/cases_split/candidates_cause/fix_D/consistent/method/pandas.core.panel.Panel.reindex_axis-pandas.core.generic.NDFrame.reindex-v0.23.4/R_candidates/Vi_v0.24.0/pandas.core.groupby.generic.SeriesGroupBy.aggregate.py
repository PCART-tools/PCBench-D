    @Substitution(see_also=_agg_see_also_doc,
                  examples=_agg_examples_doc,
                  versionadded='',
                  klass='Series',
                  axis='')
    @Appender(_shared_docs['aggregate'])
    def aggregate(self, func_or_funcs, *args, **kwargs):
        _level = kwargs.pop('_level', None)
        if isinstance(func_or_funcs, compat.string_types):
            return getattr(self, func_or_funcs)(*args, **kwargs)

        if isinstance(func_or_funcs, compat.Iterable):
            # Catch instances of lists / tuples
            # but not the class list / tuple itself.
            ret = self._aggregate_multiple_funcs(func_or_funcs,
                                                 (_level or 0) + 1)
        else:
            cyfunc = self._is_cython_func(func_or_funcs)
            if cyfunc and not args and not kwargs:
                return getattr(self, cyfunc)()

            if self.grouper.nkeys > 1:
                return self._python_agg_general(func_or_funcs, *args, **kwargs)

            try:
                return self._python_agg_general(func_or_funcs, *args, **kwargs)
            except Exception:
                result = self._aggregate_named(func_or_funcs, *args, **kwargs)

            index = Index(sorted(result), name=self.grouper.names[0])
            ret = Series(result, index=index)

        if not self.as_index:  # pragma: no cover
            print('Warning, ignoring as_index=True')

        # _level handled at higher
        if not _level and isinstance(ret, dict):
            from pandas import concat
            ret = concat(ret, axis=1)
        return ret
