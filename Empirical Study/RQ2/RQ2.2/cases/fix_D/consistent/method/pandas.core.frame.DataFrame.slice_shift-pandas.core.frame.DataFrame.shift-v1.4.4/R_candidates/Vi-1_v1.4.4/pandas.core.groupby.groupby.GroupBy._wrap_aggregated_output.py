    @final
    def _wrap_aggregated_output(
        self,
        output: Series | DataFrame | Mapping[base.OutputKey, ArrayLike],
        qs: npt.NDArray[np.float64] | None = None,
    ):
        """
        Wraps the output of GroupBy aggregations into the expected result.

        Parameters
        ----------
        output : Series, DataFrame, or Mapping[base.OutputKey, ArrayLike]
           Data to wrap.

        Returns
        -------
        Series or DataFrame
        """

        if isinstance(output, (Series, DataFrame)):
            # We get here (for DataFrameGroupBy) if we used Manager.grouped_reduce,
            #  in which case our columns are already set correctly.
            # ATM we do not get here for SeriesGroupBy; when we do, we will
            #  need to require that result.name already match self.obj.name
            result = output
        else:
            result = self._indexed_output_to_ndframe(output)

        if not self.as_index:
            # `not self.as_index` is only relevant for DataFrameGroupBy,
            #   enforced in __init__
            self._insert_inaxis_grouper_inplace(result)
            result = result._consolidate()
            index = Index(range(self.grouper.ngroups))

        else:
            index = self.grouper.result_index

        if qs is not None:
            # We get here with len(qs) != 1 and not self.as_index
            #  in test_pass_args_kwargs
            index = _insert_quantile_level(index, qs)

        result.index = index

        if self.axis == 1:
            # Only relevant for DataFrameGroupBy, no-op for SeriesGroupBy
            result = result.T
            if result.index.equals(self.obj.index):
                # Retain e.g. DatetimeIndex/TimedeltaIndex freq
                result.index = self.obj.index.copy()
                # TODO: Do this more systematically

        return self._reindex_output(result, qs=qs)
