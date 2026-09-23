    def _wrap_transformed_output(
        self, output: Mapping[base.OutputKey, Union[Series, np.ndarray]]
    ) -> Series:
        """
        Wraps the output of a SeriesGroupBy aggregation into the expected result.

        Parameters
        ----------
        output : dict[base.OutputKey, Union[Series, np.ndarray]]
            Dict with a sole key of 0 and a value of the result values.

        Returns
        -------
        Series

        Notes
        -----
        output should always contain one element. It is specified as a dict
        for consistency with DataFrame methods and _wrap_aggregated_output.
        """
        assert len(output) == 1
        result = self._wrap_series_output(output=output, index=self.obj.index)

        # No transformations increase the ndim of the result
        assert isinstance(result, Series)
        return result
