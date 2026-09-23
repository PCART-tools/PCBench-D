    def _wrap_series_output(
        self, output: Mapping[base.OutputKey, Union[Series, np.ndarray]], index: Index
    ) -> Union[Series, DataFrame]:
        """
        Wraps the output of a SeriesGroupBy operation into the expected result.

        Parameters
        ----------
        output : Mapping[base.OutputKey, Union[Series, np.ndarray]]
            Data to wrap.
        index : pd.Index
            Index to apply to the output.

        Returns
        -------
        Series or DataFrame

        Notes
        -----
        In the vast majority of cases output and columns will only contain one
        element. The exception is operations that expand dimensions, like ohlc.
        """
        indexed_output = {key.position: val for key, val in output.items()}
        columns = Index(key.label for key in output)

        result: Union[Series, DataFrame]
        if len(output) > 1:
            result = DataFrame(indexed_output, index=index)
            result.columns = columns
        else:
            result = Series(indexed_output[0], index=index, name=columns[0])

        return result
