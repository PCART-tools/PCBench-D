    def _sub_datetimelike_scalar(self, other):
        # Overridden by DatetimeArray
        assert other is not NaT
        raise TypeError("cannot subtract a datelike from a {cls}"
                        .format(cls=type(self).__name__))
