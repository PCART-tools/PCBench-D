    def __setitem__(self, attr, value):
        raise ValueError("cannot set items on {0}".format(
            self.__class__.__name__))
