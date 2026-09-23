    def _add_datelike(self, other):
        raise TypeError("cannot add {0} and {1}"
                        .format(type(self).__name__,
                                type(other).__name__))
