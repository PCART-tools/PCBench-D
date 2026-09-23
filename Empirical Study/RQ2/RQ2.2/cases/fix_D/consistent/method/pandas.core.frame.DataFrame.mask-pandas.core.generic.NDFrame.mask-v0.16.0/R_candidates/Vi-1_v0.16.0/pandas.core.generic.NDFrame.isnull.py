    def isnull(self):
        """
        Return a boolean same-sized object indicating if the values are null

        See also
        --------
        notnull : boolean inverse of isnull
        """
        return isnull(self).__finalize__(self)
