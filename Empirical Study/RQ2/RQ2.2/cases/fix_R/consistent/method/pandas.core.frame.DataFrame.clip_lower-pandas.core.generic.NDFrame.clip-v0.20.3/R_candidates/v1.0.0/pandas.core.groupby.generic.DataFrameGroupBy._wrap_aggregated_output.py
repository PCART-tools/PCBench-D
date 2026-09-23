    def _wrap_aggregated_output(
        self, output: Mapping[base.OutputKey, Union[Series, np.ndarray]]
    ) -> DataFrame:
        """
        Wraps the output of DataFrameGroupBy aggregations into the expected result.

        Parameters
        ----------
        output : Mapping[base.OutputKey, Union[Series, np.ndarray]]
           Data to wrap.

        Returns
        -------
        DataFrame
        """
        indexed_output = {key.position: val for key, val in output.items()}
        columns = Index(key.label for key in output)

        result = DataFrame(indexed_output)
        result.columns = columns

        if not self.as_index:
            self._insert_inaxis_grouper_inplace(result)
            result = result._consolidate()
        else:
            index = self.grouper.result_index
            result.index = index

        if self.axis == 1:
            result = result.T

        return self._reindex_output(result)._convert(datetime=True)
