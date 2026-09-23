    def __mul__(self, other):
        return self.__class__(super(FrozenList, self).__mul__(other))
