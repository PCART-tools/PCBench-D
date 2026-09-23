    def _construct_result(self, result) -> "DataFrame":
        """
        Wrap the result of an arithmetic, comparison, or logical operation.

        Parameters
        ----------
        result : DataFrame

        Returns
        -------
        DataFrame
        """
        out = self._constructor(result, index=self.index, copy=False)
        # Pin columns instead of passing to constructor for compat with
        #  non-unique columns case
        out.columns = self.columns
        return out
