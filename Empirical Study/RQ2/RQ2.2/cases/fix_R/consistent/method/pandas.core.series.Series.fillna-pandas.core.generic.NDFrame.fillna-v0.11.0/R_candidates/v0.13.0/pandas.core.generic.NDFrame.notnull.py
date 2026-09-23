    def notnull(self):
        """Return a boolean same-sized object indicating if the values are
        not null
        """
        return notnull(self).__finalize__(self)
