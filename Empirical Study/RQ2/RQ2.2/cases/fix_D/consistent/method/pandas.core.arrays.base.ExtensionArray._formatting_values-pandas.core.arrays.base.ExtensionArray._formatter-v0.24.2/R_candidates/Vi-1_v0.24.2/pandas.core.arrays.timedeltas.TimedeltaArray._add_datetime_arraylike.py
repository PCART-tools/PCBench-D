    def _add_datetime_arraylike(self, other):
        """
        Add DatetimeArray/Index or ndarray[datetime64] to TimedeltaArray.
        """
        if isinstance(other, np.ndarray):
            # At this point we have already checked that dtype is datetime64
            from pandas.core.arrays import DatetimeArray
            other = DatetimeArray(other)

        # defer to implementation in DatetimeArray
        return other + self
