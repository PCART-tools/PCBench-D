    def isna(self):
        """
        Detect missing values

        Missing values (-1 in .codes) are detected.

        Returns
        -------
        a boolean array of whether my values are null

        See Also
        --------
        isna : Top-level isna.
        isnull : Alias of isna.
        Categorical.notna : Boolean inverse of Categorical.isna.

        """

        ret = self._codes == -1
        return ret
