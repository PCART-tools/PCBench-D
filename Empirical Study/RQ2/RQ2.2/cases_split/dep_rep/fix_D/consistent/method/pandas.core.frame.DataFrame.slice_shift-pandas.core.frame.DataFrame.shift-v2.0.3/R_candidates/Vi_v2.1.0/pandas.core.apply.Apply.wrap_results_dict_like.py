    def wrap_results_dict_like(
        self,
        selected_obj: Series | DataFrame,
        result_index: list[Hashable],
        result_data: list,
    ):
        from pandas import Index
        from pandas.core.reshape.concat import concat

        obj = self.obj

        # Avoid making two isinstance calls in all and any below
        is_ndframe = [isinstance(r, ABCNDFrame) for r in result_data]

        if all(is_ndframe):
            results = dict(zip(result_index, result_data))
            keys_to_use: Iterable[Hashable]
            keys_to_use = [k for k in result_index if not results[k].empty]
            # Have to check, if at least one DataFrame is not empty.
            keys_to_use = keys_to_use if keys_to_use != [] else result_index
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

            # we have a list of scalars
            # GH 36212 use name only if obj is a series
            if obj.ndim == 1:
                obj = cast("Series", obj)
                name = obj.name
            else:
                name = None

            result = Series(result_data, index=result_index, name=name)

        return result
