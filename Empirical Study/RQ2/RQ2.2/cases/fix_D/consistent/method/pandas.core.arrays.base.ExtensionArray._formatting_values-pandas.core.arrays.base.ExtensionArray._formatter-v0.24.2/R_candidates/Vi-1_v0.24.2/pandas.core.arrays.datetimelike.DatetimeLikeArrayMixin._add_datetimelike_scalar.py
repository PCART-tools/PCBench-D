    def _add_datetimelike_scalar(self, other):
        # Overriden by TimedeltaArray
        raise TypeError("cannot add {cls} and {typ}"
                        .format(cls=type(self).__name__,
                                typ=type(other).__name__))
