    @final
    def _get_arithmetic_result_freq(self, other) -> BaseOffset | None:
        """
        Check if we can preserve self.freq in addition or subtraction.
        """
        # Adding or subtracting a Timedelta/Timestamp scalar is freq-preserving
        #  whenever self.freq is a Tick
        if is_period_dtype(self.dtype):
            return self.freq
        elif not lib.is_scalar(other):
            return None
        elif isinstance(self.freq, Tick):
            # In these cases
            return self.freq
        return None
