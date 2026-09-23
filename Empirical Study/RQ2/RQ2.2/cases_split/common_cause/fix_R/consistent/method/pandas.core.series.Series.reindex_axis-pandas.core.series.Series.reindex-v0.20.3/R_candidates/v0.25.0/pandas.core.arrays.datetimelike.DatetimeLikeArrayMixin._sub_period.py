    def _sub_period(self, other):
        # Overriden by PeriodArray
        raise TypeError(
            "cannot subtract Period from a {cls}".format(cls=type(self).__name__)
        )
