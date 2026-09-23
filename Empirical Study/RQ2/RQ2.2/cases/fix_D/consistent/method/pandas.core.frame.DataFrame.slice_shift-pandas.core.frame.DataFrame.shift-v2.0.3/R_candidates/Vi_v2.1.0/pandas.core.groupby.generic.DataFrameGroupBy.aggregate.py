    @doc(_agg_template_frame, examples=_agg_examples_doc, klass="DataFrame")
    def aggregate(self, func=None, *args, engine=None, engine_kwargs=None, **kwargs):
        relabeling, func, columns, order = reconstruct_func(func, **kwargs)
        func = maybe_mangle_lambdas(func)

        if maybe_use_numba(engine):
            # Not all agg functions support numba, only propagate numba kwargs
            # if user asks for numba
            kwargs["engine"] = engine
            kwargs["engine_kwargs"] = engine_kwargs

        op = GroupByApply(self, func, args=args, kwargs=kwargs)
        result = op.agg()
        if not is_dict_like(func) and result is not None:
            # GH #52849
            if not self.as_index and is_list_like(func):
                return result.reset_index()
            else:
                return result
        elif relabeling:
            # this should be the only (non-raising) case with relabeling
            # used reordered index of columns
            result = cast(DataFrame, result)
            result = result.iloc[:, order]
            result = cast(DataFrame, result)
            # error: Incompatible types in assignment (expression has type
            # "Optional[List[str]]", variable has type
            # "Union[Union[Union[ExtensionArray, ndarray[Any, Any]],
            # Index, Series], Sequence[Any]]")
            result.columns = columns  # type: ignore[assignment]

        if result is None:
            # Remove the kwargs we inserted
            # (already stored in engine, engine_kwargs arguments)
            if "engine" in kwargs:
                del kwargs["engine"]
                del kwargs["engine_kwargs"]
            # at this point func is not a str, list-like, dict-like,
            # or a known callable(e.g. sum)
            if maybe_use_numba(engine):
                return self._aggregate_with_numba(
                    func, *args, engine_kwargs=engine_kwargs, **kwargs
                )
            # grouper specific aggregations
            if self.grouper.nkeys > 1:
                # test_groupby_as_index_series_scalar gets here with 'not self.as_index'
                return self._python_agg_general(func, *args, **kwargs)
            elif args or kwargs:
                # test_pass_args_kwargs gets here (with and without as_index)
                # can't return early
                result = self._aggregate_frame(func, *args, **kwargs)

            elif self.axis == 1:
                # _aggregate_multiple_funcs does not allow self.axis == 1
                # Note: axis == 1 precludes 'not self.as_index', see __init__
                result = self._aggregate_frame(func)
                return result

            else:
                # try to treat as if we are passing a list
                gba = GroupByApply(self, [func], args=(), kwargs={})
                try:
                    result = gba.agg()

                except ValueError as err:
                    if "No objects to concatenate" not in str(err):
                        raise
                    # _aggregate_frame can fail with e.g. func=Series.mode,
                    # where it expects 1D values but would be getting 2D values
                    # In other tests, using aggregate_frame instead of GroupByApply
                    #  would give correct values but incorrect dtypes
                    #  object vs float64 in test_cython_agg_empty_buckets
                    #  float64 vs int64 in test_category_order_apply
                    result = self._aggregate_frame(func)

                else:
                    # GH#32040, GH#35246
                    # e.g. test_groupby_as_index_select_column_sum_empty_df
                    result = cast(DataFrame, result)
                    result.columns = self._obj_with_exclusions.columns.copy()

        if not self.as_index:
            result = self._insert_inaxis_grouper(result)
            result.index = default_index(len(result))

        return result
