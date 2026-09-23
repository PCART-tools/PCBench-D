    def agg_list_like(self) -> DataFrame | Series:
        """
        Compute aggregation in the case of a list-like argument.

        Returns
        -------
        Result of aggregation.
        """
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
        failed_names = []

        depr_nuisance_columns_msg = (
            "{} did not aggregate successfully. If any error is "
            "raised this will raise in a future version of pandas. "
            "Drop these columns/ops to avoid this warning."
        )

        # degenerate case
        if selected_obj.ndim == 1:
            for a in arg:
                colg = obj._gotitem(selected_obj.name, ndim=1, subset=selected_obj)
                try:
                    new_res = colg.aggregate(a)

                except TypeError:
                    failed_names.append(com.get_callable_name(a) or a)
                else:
                    results.append(new_res)

                    # make sure we find a good name
                    name = com.get_callable_name(a) or a
                    keys.append(name)

        # multiples
        else:
            indices = []
            for index, col in enumerate(selected_obj):
                colg = obj._gotitem(col, ndim=1, subset=selected_obj.iloc[:, index])
                try:
                    # Capture and suppress any warnings emitted by us in the call
                    # to agg below, but pass through any warnings that were
                    # generated otherwise.
                    # This is necessary because of https://bugs.python.org/issue29672
                    # See GH #43741 for more details
                    with warnings.catch_warnings(record=True) as record:
                        new_res = colg.aggregate(arg)
                    if len(record) > 0:
                        match = re.compile(depr_nuisance_columns_msg.format(".*"))
                        for warning in record:
                            if re.match(match, str(warning.message)):
                                failed_names.append(col)
                            else:
                                warnings.warn_explicit(
                                    message=warning.message,
                                    category=warning.category,
                                    filename=warning.filename,
                                    lineno=warning.lineno,
                                )

                except (TypeError, DataError):
                    failed_names.append(col)
                except ValueError as err:
                    # cannot aggregate
                    if "Must produce aggregated value" in str(err):
                        # raised directly in _aggregate_named
                        failed_names.append(col)
                    elif "no results" in str(err):
                        # reached in test_frame_apply.test_nuiscance_columns
                        #  where the colg.aggregate(arg) ends up going through
                        #  the selected_obj.ndim == 1 branch above with arg == ["sum"]
                        #  on a datetime64[ns] column
                        failed_names.append(col)
                    else:
                        raise
                else:
                    results.append(new_res)
                    indices.append(index)

            keys = selected_obj.columns.take(indices)

        # if we are empty
        if not len(results):
            raise ValueError("no results")

        if len(failed_names) > 0:
            warnings.warn(
                depr_nuisance_columns_msg.format(failed_names),
                FutureWarning,
                stacklevel=find_stack_level(),
            )

        try:
            concatenated = concat(results, keys=keys, axis=1, sort=False)
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
        else:
            # Concat uses the first index to determine the final indexing order.
            # The union of a shorter first index with the other indices causes
            # the index sorting to be different from the order of the aggregating
            # functions. Reindex if this is the case.
            index_size = concatenated.index.size
            full_ordered_index = next(
                result.index for result in results if result.index.size == index_size
            )
            return concatenated.reindex(full_ordered_index, copy=False)
