    def isnull(self):
        """
        Return a boolean same-sized object indicating if the values are null
        """
        return isnull(self).__finalize__(self)
