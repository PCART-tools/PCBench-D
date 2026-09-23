    def notnull(self):
        """Return a boolean same-sized object indicating if the values are
        not null

        See also
        --------
        isnull : boolean inverse of notnull
        """
        return notnull(self).__finalize__(self)
