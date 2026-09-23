    def _sub_period(self, other):
        # Overridden by PeriodArray
        raise TypeError(f"cannot subtract Period from a {type(self).__name__}")
