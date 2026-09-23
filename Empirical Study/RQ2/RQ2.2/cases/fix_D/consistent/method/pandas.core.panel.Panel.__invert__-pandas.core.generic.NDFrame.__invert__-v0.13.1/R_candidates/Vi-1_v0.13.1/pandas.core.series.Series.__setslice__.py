    def __setslice__(self, i, j, value):
        """Set slice equal to given value(s)"""
        if i < 0:
            i = 0
        if j < 0:
            j = 0
        slobj = slice(i, j)
        return self.__setitem__(slobj, value)
