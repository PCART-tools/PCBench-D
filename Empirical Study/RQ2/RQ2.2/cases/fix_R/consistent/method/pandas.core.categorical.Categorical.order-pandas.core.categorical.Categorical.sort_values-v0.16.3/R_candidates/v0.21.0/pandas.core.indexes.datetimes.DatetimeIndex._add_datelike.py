    def _add_datelike(self, other):
        # adding a timedeltaindex to a datetimelike
        if other is libts.NaT:
            return self._nat_new(box=True)
        raise TypeError("cannot add {0} and {1}"
                        .format(type(self).__name__,
                                type(other).__name__))
