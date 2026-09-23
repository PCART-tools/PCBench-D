    def _add_period(self, other: Period):
        # Overridden by TimedeltaArray
        raise TypeError(f"cannot add Period to a {type(self).__name__}")
