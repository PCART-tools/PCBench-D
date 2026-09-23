    def __hash__(self):
        raise TypeError('{0!r} objects are mutable, thus they cannot be'
                        ' hashed'.format(self.__class__.__name__))
