    @property
    def base(self):
        """ return the base object if the memory of the underlying data is shared """
        return self.values.base
