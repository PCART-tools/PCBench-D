    def agg_list_like(self) -> DataFrame | Series:
        """
        Compute aggregation in the case of a list-like argument.

        Returns
        -------
        Result of aggregation.
        """
        from pandas.core.groupby.generic import (
            DataFrameGroupBy,
            SeriesGroupBy,
        )
        from pandas.core.reshape.concat import concat

        obj = self.obj
        arg = cast(List[AggFuncTypeBase], self.f)

        if getattr(obj, "axis", 0) == 1:
            raise NotImplementedError("axis other than 0 is not supported")

        if not isinstance(obj, SelectionMixin):
            # i.e. obj is Series or DataFrame
            selected_obj = obj
        elif obj._selected_obj.ndim == 1:
            # For SeriesGroupBy this matches _obj_with_exclusions
            selected_obj = obj._selected_obj
        else:
            selected_obj = obj._obj_with_exclusions

        results = []
        keys = []

        is_groupby = isinstance(obj, (DataFrameGroupBy, SeriesGroupBy))
        context_manager: ContextManager
        if is_groupby:
            # When as_index=False, we combine all results using indices
            # and adjust index after
            context_manager = com.temp_setattr(obj, "as_index", True)
        else:
            context_manager = nullcontext()
        with context_manager:
            # degenerate case
            if selected_obj.ndim == 1:
                for a in arg:
                    colg = obj._gotitem(selected_obj.name, ndim=1, subset=selected_obj)
                    if isinstance(colg, (ABCSeries, ABCDataFrame)):
                        new_res = colg.aggregate(
                            a, self.axis, *self.args, **self.kwargs
                        )
                    else:
                        new_res = colg.aggregate(a, *self.args, **self.kwargs)
                    results.append(new_res)

                    # make sure we find a good name
                    name = com.get_callable_name(a) or a
                    keys.append(name)

            else:
                indices = []
                for index, col in enumerate(selected_obj):
                    colg = obj._gotitem(col, ndim=1, subset=selected_obj.iloc[:, index])
                    if isinstance(colg, (ABCSeries, ABCDataFrame)):
                        new_res = colg.aggregate(
                            arg, self.axis, *self.args, **self.kwargs
                        )
                    else:
                        new_res = colg.aggregate(arg, *self.args, **self.kwargs)
                    results.append(new_res)
                    indices.append(index)
                keys = selected_obj.columns.take(indices)

        try:
            return concat(results, keys=keys, axis=1, sort=False)
        except TypeError as err:
            # we are concatting non-NDFrame objects,
            # e.g. a list of scalars
            from pandas import Series

            result = Series(results, index=keys, name=obj.name)
            if is_nested_object(result):
                raise ValueError(
                    "cannot combine transform and aggregation operations"
                ) from err
            return result
