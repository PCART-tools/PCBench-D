    def _is_comparable_dtype(self, dtype: DtypeObj) -> bool:
        """
        Can we compare values of the given dtype to our own?
        """
        if self.tz is not None:
            # If we have tz, we can compare to tzaware
            return is_datetime64tz_dtype(dtype)
        # if we dont have tz, we can only compare to tznaive
        return is_datetime64_dtype(dtype)
