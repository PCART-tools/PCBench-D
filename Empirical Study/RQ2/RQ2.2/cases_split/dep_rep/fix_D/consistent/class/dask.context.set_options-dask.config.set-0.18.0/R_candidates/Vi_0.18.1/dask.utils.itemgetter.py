class itemgetter(object):
    """
    Return a callable object that gets an item from the operand

    Unlike the builtin `operator.itemgetter`, instances of this class are
    serializable
    """
    __slots__ = ('index',)

    def __init__(self, index):
        self.index = index

    def __call__(self, x):
        return x[self.index]

    def __reduce__(self):
        return (itemgetter, (self.index,))

    def __eq__(self, other):
        return type(self) is type(other) and self.index == other.index
