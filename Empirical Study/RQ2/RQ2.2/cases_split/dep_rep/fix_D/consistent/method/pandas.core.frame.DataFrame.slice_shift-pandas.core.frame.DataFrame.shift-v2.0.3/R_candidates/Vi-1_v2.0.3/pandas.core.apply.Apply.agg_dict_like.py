    def agg_dict_like(self) -> DataFrame | Series:
        """
        Compute aggregation in the case of a dict-like argument.

        Returns
        -------
        Result of aggregation.
        """
        from pandas import Index
        from pandas.core.groupby.generic import (
            DataFrameGroupBy,
            SeriesGroupBy,
        )
        from pandas.core.reshape.concat import concat

        obj = self.obj
        arg = cast(AggFuncTypeDict, self.f)

        if getattr(obj, "axis", 0) == 1:
            raise NotImplementedError("axis other than 0 is not supported")

        if not isinstance(obj, SelectionMixin):
            # i.e. obj is Series or DataFrame
            selected_obj = obj
            selection = None
        else:
            selected_obj = obj._selected_obj
            selection = obj._selection

        arg = self.normalize_dictlike_arg("agg", selected_obj, arg)

        is_groupby = isinstance(obj, (DataFrameGroupBy, SeriesGroupBy))
        context_manager: ContextManager
        if is_groupby:
            # When as_index=False, we combine all results using indices
            # and adjust index after
            context_manager = com.temp_setattr(obj, "as_index", True)
        else:
            context_manager = nullcontext()
        with context_manager:
            if selected_obj.ndim == 1:
                # key only used for output
                colg = obj._gotitem(selection, ndim=1)
                results = {key: colg.agg(how) for key, how in arg.items()}
            else:
                # key used for column selection and output
                results = {
                    key: obj._gotitem(key, ndim=1).agg(how) for key, how in arg.items()
                }

        # set the final keys
        keys = list(arg.keys())

        # Avoid making two isinstance calls in all and any below
        is_ndframe = [isinstance(r, ABCNDFrame) for r in results.values()]

        # combine results
        if all(is_ndframe):
            keys_to_use: Iterable[Hashable]
            keys_to_use = [k for k in keys if not results[k].empty]
            # Have to check, if at least one DataFrame is not empty.
            keys_to_use = keys_to_use if keys_to_use != [] else keys
            if selected_obj.ndim == 2:
                # keys are columns, so we can preserve names
                ktu = Index(keys_to_use)
                ktu._set_names(selected_obj.columns.names)
                keys_to_use = ktu

            axis: AxisInt = 0 if isinstance(obj, ABCSeries) else 1
            result = concat(
                {k: results[k] for k in keys_to_use},
                axis=axis,
                keys=keys_to_use,
            )
        elif any(is_ndframe):
            # There is a mix of NDFrames and scalars
            raise ValueError(
                "cannot perform both aggregation "
                "and transformation operations "
                "simultaneously"
            )
        else:
            from pandas import Series

            # we have a dict of scalars
            # GH 36212 use name only if obj is a series
            if obj.ndim == 1:
                obj = cast("Series", obj)
                name = obj.name
            else:
                name = None

            result = Series(results, name=name)

        return result
