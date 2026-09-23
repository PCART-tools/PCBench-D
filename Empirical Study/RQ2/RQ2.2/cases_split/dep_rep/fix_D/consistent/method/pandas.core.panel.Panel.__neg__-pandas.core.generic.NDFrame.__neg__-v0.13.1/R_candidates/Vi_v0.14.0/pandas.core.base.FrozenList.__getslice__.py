    def __getslice__(self, i, j):
        return self.__class__(super(FrozenList, self).__getslice__(i, j))
