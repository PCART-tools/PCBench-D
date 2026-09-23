    def __getitem__(self, n):
        # Python 3 compat
        if isinstance(n, slice):
            return self.__class__(super().__getitem__(n))
        return super().__getitem__(n)
