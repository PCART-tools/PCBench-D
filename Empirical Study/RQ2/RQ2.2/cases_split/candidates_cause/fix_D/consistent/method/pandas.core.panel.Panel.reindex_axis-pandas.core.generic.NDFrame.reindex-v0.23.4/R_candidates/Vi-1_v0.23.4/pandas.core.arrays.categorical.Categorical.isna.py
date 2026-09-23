    def isna(self):
        """
        Detect missing values

        Missing values (-1 in .codes) are detected.

        Returns
        -------
        a boolean array of whether my values are null

        See also
        --------
        isna : top-level isna
        isnull : alias of isna
        Categorical.notna : boolean inverse of Categorical.isna

        """

        ret = self._codes == -1
        return ret
