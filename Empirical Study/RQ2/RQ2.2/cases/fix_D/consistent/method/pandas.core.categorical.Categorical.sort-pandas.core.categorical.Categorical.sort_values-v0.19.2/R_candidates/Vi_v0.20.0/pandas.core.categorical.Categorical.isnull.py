    def isnull(self):
        """
        Detect missing values

        Both missing values (-1 in .codes) and NA as a category are detected.

        Returns
        -------
        a boolean array of whether my values are null

        See also
        --------
        isnull : pandas version
        Categorical.notnull : boolean inverse of Categorical.isnull

        """

        ret = self._codes == -1

        # String/object and float categories can hold np.nan
        if self.categories.dtype.kind in ['S', 'O', 'f']:
            if np.nan in self.categories:
                nan_pos = np.where(isnull(self.categories))[0]
                # we only have one NA in categories
                ret = np.logical_or(ret, self._codes == nan_pos)
        return ret
