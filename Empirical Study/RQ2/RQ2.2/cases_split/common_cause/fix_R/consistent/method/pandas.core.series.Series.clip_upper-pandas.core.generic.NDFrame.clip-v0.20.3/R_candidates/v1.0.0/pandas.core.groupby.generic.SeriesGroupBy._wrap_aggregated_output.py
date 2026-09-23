    def _wrap_aggregated_output(
        self, output: Mapping[base.OutputKey, Union[Series, np.ndarray]]
    ) -> Union[Series, DataFrame]:
        """
        Wraps the output of a SeriesGroupBy aggregation into the expected result.

        Parameters
        ----------
        output : Mapping[base.OutputKey, Union[Series, np.ndarray]]
            Data to wrap.

        Returns
        -------
        Series or DataFrame

        Notes
        -----
        In the vast majority of cases output will only contain one element.
        The exception is operations that expand dimensions, like ohlc.
        """
        result = self._wrap_series_output(
            output=output, index=self.grouper.result_index
        )
        return self._reindex_output(result)._convert(datetime=True)
