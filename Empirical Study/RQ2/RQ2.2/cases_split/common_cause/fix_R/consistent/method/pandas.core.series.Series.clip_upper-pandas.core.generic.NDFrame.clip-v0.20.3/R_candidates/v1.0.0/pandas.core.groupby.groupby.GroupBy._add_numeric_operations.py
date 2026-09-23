    @classmethod
    def _add_numeric_operations(cls):
        """
        Add numeric operations to the GroupBy generically.
        """

        def groupby_function(
            name: str,
            alias: str,
            npfunc,
            numeric_only: bool = True,
            min_count: int = -1,
        ):

            _local_template = """
            Compute %(f)s of group values.

            Returns
            -------
            Series or DataFrame
                Computed %(f)s of values within each group.
            """

            @Substitution(name="groupby", f=name)
            @Appender(_common_see_also)
            @Appender(_local_template)
            def f(self, **kwargs):
                if "numeric_only" not in kwargs:
                    kwargs["numeric_only"] = numeric_only
                if "min_count" not in kwargs:
                    kwargs["min_count"] = min_count

                self._set_group_selection()

                # try a cython aggregation if we can
                try:
                    return self._cython_agg_general(alias, alt=npfunc, **kwargs)
                except DataError:
                    pass
                except NotImplementedError as err:
                    if "function is not implemented for this dtype" in str(err):
                        # raised in _get_cython_function, in some cases can
                        #  be trimmed by implementing cython funcs for more dtypes
                        pass
                    else:
                        raise

                # apply a non-cython aggregation
                result = self.aggregate(lambda x: npfunc(x, axis=self.axis))
                return result

            set_function_name(f, name, cls)

            return f

        def first_compat(x, axis=0):
            def first(x):
                x = x.to_numpy()

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
                x = x.to_numpy()
                x = x[notna(x)]
                if len(x) == 0:
                    return np.nan
                return x[-1]

            if isinstance(x, DataFrame):
                return x.apply(last, axis=axis)
            else:
                return last(x)

        cls.sum = groupby_function("sum", "add", np.sum, min_count=0)
        cls.prod = groupby_function("prod", "prod", np.prod, min_count=0)
        cls.min = groupby_function("min", "min", np.min, numeric_only=False)
        cls.max = groupby_function("max", "max", np.max, numeric_only=False)
        cls.first = groupby_function("first", "first", first_compat, numeric_only=False)
        cls.last = groupby_function("last", "last", last_compat, numeric_only=False)
