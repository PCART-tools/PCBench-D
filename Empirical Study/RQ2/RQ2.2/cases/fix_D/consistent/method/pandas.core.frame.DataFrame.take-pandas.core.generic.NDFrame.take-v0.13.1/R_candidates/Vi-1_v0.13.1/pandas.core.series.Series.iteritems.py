    def iteritems(self):
        """
        Lazily iterate over (index, value) tuples
        """
        return lzip(iter(self.index), iter(self))
