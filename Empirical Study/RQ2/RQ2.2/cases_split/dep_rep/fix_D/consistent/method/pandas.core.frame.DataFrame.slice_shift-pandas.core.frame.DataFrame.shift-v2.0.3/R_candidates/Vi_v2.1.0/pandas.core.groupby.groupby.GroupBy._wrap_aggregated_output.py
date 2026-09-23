    @final
    def _wrap_aggregated_output(
        self,
        result: Series | DataFrame,
        qs: npt.NDArray[np.float64] | None = None,
    ):
        """
        Wraps the output of GroupBy aggregations into the expected result.

        Parameters
        ----------
        result : Series, DataFrame

        Returns
        -------
        Series or DataFrame
        """
        # ATM we do not get here for SeriesGroupBy; when we do, we will
        #  need to require that result.name already match self.obj.name

        if not self.as_index:
            # `not self.as_index` is only relevant for DataFrameGroupBy,
            #   enforced in __init__
            result = self._insert_inaxis_grouper(result)
            result = result._consolidate()
            index = Index(range(self.grouper.ngroups))

        else:
            index = self.grouper.result_index

        if qs is not None:
            # We get here with len(qs) != 1 and not self.as_index
            #  in test_pass_args_kwargs
            index = _insert_quantile_level(index, qs)

        result.index = index

        # error: Argument 1 to "_maybe_transpose_result" of "GroupBy" has
        # incompatible type "Union[Series, DataFrame]"; expected "NDFrameT"
        res = self._maybe_transpose_result(result)  # type: ignore[arg-type]
        return self._reindex_output(res, qs=qs)
