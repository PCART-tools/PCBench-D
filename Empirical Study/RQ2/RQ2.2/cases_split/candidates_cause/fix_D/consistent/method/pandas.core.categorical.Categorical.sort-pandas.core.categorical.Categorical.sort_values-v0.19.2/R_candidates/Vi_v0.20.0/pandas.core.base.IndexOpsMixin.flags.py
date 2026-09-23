    @property
    def flags(self):
        """ return the ndarray.flags for the underlying data """
        return self.values.flags
