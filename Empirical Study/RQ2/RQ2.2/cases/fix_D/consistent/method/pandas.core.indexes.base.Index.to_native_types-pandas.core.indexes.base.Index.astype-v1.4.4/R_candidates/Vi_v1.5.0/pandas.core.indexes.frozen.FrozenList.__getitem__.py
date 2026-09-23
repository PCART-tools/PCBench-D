    def __getitem__(self, n):
        if isinstance(n, slice):
            return type(self)(super().__getitem__(n))
        return super().__getitem__(n)
