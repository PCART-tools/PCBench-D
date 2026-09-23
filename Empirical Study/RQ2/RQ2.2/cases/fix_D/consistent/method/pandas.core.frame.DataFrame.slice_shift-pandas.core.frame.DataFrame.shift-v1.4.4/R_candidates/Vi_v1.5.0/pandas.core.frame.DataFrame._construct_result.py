    def _construct_result(self, result) -> DataFrame:
        """
        Wrap the result of an arithmetic, comparison, or logical operation.

        Parameters
        ----------
        result : DataFrame

        Returns
        -------
        DataFrame
        """
        out = self._constructor(result, copy=False)
        # Pin columns instead of passing to constructor for compat with
        #  non-unique columns case
        out.columns = self.columns
        out.index = self.index
        return out
