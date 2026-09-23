    def notnull(self):
        """
        Reverse of isnull

        Both missing values (-1 in .codes) and NA as a category are detected as
        null.

        Returns
        -------
        a boolean array of whether my values are not null

        See also
        --------
        pandas.notnull : pandas version
        Categorical.isnull : boolean inverse of Categorical.notnull
        """
        return ~self.isnull()
