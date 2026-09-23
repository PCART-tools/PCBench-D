    def notna(self):
        """
        Inverse of isna

        Both missing values (-1 in .codes) and NA as a category are detected as
        null.

        Returns
        -------
        a boolean array of whether my values are not null

        See also
        --------
        notna : top-level notna
        notnull : alias of notna
        Categorical.isna : boolean inverse of Categorical.notna

        """
        return ~self.isna()
