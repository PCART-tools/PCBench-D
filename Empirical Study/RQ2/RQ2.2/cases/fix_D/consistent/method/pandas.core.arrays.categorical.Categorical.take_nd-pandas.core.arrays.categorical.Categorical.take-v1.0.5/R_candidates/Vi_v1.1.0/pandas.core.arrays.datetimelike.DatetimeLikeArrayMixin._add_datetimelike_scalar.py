    def _add_datetimelike_scalar(self, other):
        # Overridden by TimedeltaArray
        raise TypeError(f"cannot add {type(self).__name__} and {type(other).__name__}")
