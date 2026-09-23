    @final
    def _wrap_transformed_output(
        self, output: Mapping[base.OutputKey, ArrayLike]
    ) -> Series | DataFrame:
        """
        Wraps the output of GroupBy transformations into the expected result.

        Parameters
        ----------
        output : Mapping[base.OutputKey, ArrayLike]
            Data to wrap.

        Returns
        -------
        Series or DataFrame
            Series for SeriesGroupBy, DataFrame for DataFrameGroupBy
        """
        if isinstance(output, (Series, DataFrame)):
            result = output
        else:
            result = self._indexed_output_to_ndframe(output)

        if self.axis == 1:
            # Only relevant for DataFrameGroupBy
            result = result.T
            result.columns = self.obj.columns

        result.index = self.obj.index
        return result
