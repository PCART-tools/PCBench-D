    def _sub_period_array(self, other):
        # Overridden by PeriodArray
        raise TypeError(
            f"cannot subtract {other.dtype}-dtype from {type(self).__name__}"
        )
