    def _add_datelike(self, other):
        raise TypeError("cannot add {cls} and {typ}"
                        .format(cls=type(self).__name__,
                                typ=type(other).__name__))
