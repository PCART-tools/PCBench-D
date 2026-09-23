    def __getslice__(self, i, j):
        return self.__class__(super().__getslice__(i, j))
