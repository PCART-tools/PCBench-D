    @final
    def _reindex_output(
        self,
        output: OutputFrameOrSeries,
        fill_value: Scalar = np.NaN,
        qs: npt.NDArray[np.float64] | None = None,
    ) -> OutputFrameOrSeries:
        """
        If we have categorical groupers, then we might want to make sure that
        we have a fully re-indexed output to the levels. This means expanding
        the output space to accommodate all values in the cartesian product of
        our groups, regardless of whether they were observed in the data or
        not. This will expand the output space if there are missing groups.

        The method returns early without modifying the input if the number of
        groupings is less than 2, self.observed == True or none of the groupers
        are categorical.

        Parameters
        ----------
        output : Series or DataFrame
            Object resulting from grouping and applying an operation.
        fill_value : scalar, default np.NaN
            Value to use for unobserved categories if self.observed is False.
        qs : np.ndarray[float64] or None, default None
            quantile values, only relevant for quantile.

        Returns
        -------
        Series or DataFrame
            Object (potentially) re-indexed to include all possible groups.
        """
        groupings = self.grouper.groupings
        if len(groupings) == 1:
            return output

        # if we only care about the observed values
        # we are done
        elif self.observed:
            return output

        # reindexing only applies to a Categorical grouper
        elif not any(
            isinstance(ping.grouping_vector, (Categorical, CategoricalIndex))
            for ping in groupings
        ):
            return output

        levels_list = [ping.group_index for ping in groupings]
        names = self.grouper.names
        if qs is not None:
            # error: Argument 1 to "append" of "list" has incompatible type
            # "ndarray[Any, dtype[floating[_64Bit]]]"; expected "Index"
            levels_list.append(qs)  # type: ignore[arg-type]
            names = names + [None]
        index, _ = MultiIndex.from_product(levels_list, names=names).sortlevel()

        if self.as_index:
            # Always holds for SeriesGroupBy unless GH#36507 is implemented
            d = {
                self.obj._get_axis_name(self.axis): index,
                "copy": False,
                "fill_value": fill_value,
            }
            return output.reindex(**d)

        # GH 13204
        # Here, the categorical in-axis groupers, which need to be fully
        # expanded, are columns in `output`. An idea is to do:
        # output = output.set_index(self.grouper.names)
        #                .reindex(index).reset_index()
        # but special care has to be taken because of possible not-in-axis
        # groupers.
        # So, we manually select and drop the in-axis grouper columns,
        # reindex `output`, and then reset the in-axis grouper columns.

        # Select in-axis groupers
        in_axis_grps = (
            (i, ping.name) for (i, ping) in enumerate(groupings) if ping.in_axis
        )
        g_nums, g_names = zip(*in_axis_grps)

        output = output.drop(labels=list(g_names), axis=1)

        # Set a temp index and reindex (possibly expanding)
        output = output.set_index(self.grouper.result_index).reindex(
            index, copy=False, fill_value=fill_value
        )

        # Reset in-axis grouper columns
        # (using level numbers `g_nums` because level names may not be unique)
        output = output.reset_index(level=g_nums)

        return output.reset_index(drop=True)
