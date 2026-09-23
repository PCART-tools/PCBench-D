    def iteritems(self):
        """
        Lazily iterate over (index, value) tuples.
        """
        return zip(iter(self.index), iter(self))
