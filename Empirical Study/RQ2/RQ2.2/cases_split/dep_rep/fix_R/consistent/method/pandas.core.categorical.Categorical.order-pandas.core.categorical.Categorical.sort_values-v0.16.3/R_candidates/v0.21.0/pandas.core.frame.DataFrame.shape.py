    @property
    def shape(self):
        """
        Return a tuple representing the dimensionality of the DataFrame.
        """
        return len(self.index), len(self.columns)
