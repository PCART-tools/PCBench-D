    def _wrap_transformed_output(
        self, output: Mapping[base.OutputKey, Union[Series, np.ndarray]]
    ) -> DataFrame:
        """
        Wraps the output of DataFrameGroupBy transformations into the expected result.

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
        result.index = self.obj.index

        return result
