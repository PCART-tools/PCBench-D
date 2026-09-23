    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))
