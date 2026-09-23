    @classmethod
    def _add_numeric_operations(cls):
        """ add numeric operations to the GroupBy generically """

        def groupby_function(name, alias, npfunc,
                             numeric_only=True, _convert=False):

            _local_template = "Compute %(f)s of group values"

            @Substitution(name='groupby', f=name)
            @Appender(_doc_template)
            @Appender(_local_template)
            def f(self, **kwargs):
                if 'numeric_only' not in kwargs:
                    kwargs['numeric_only'] = numeric_only
                self._set_group_selection()
                try:
                    return self._cython_agg_general(
                        alias, alt=npfunc, **kwargs)
                except AssertionError as e:
                    raise SpecificationError(str(e))
                except Exception:
                    result = self.aggregate(
                        lambda x: npfunc(x, axis=self.axis))
                    if _convert:
                        result = result._convert(datetime=True)
                    return result

            set_function_name(f, name, cls)

            return f

        def first_compat(x, axis=0):

            def first(x):

                x = np.asarray(x)
                x = x[notna(x)]
                if len(x) == 0:
                    return np.nan
                return x[0]

            if isinstance(x, DataFrame):
                return x.apply(first, axis=axis)
            else:
                return first(x)

        def last_compat(x, axis=0):

            def last(x):

                x = np.asarray(x)
                x = x[notna(x)]
                if len(x) == 0:
                    return np.nan
                return x[-1]

            if isinstance(x, DataFrame):
                return x.apply(last, axis=axis)
            else:
                return last(x)

        cls.sum = groupby_function('sum', 'add', np.sum)
        cls.prod = groupby_function('prod', 'prod', np.prod)
        cls.min = groupby_function('min', 'min', np.min, numeric_only=False)
        cls.max = groupby_function('max', 'max', np.max, numeric_only=False)
        cls.first = groupby_function('first', 'first', first_compat,
                                     numeric_only=False, _convert=True)
        cls.last = groupby_function('last', 'last', last_compat,
                                    numeric_only=False, _convert=True)
