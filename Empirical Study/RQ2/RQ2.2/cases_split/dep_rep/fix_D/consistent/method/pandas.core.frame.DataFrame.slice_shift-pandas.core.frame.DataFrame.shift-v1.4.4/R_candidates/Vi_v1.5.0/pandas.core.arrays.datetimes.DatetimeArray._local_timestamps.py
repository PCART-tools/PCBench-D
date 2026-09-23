    def _local_timestamps(self) -> npt.NDArray[np.int64]:
        """
        Convert to an i8 (unix-like nanosecond timestamp) representation
        while keeping the local timezone and not using UTC.
        This is used to calculate time-of-day information as if the timestamps
        were timezone-naive.
        """
        if self.tz is None or timezones.is_utc(self.tz):
            # Avoid the copy that would be made in tzconversion
            return self.asi8
        return tz_convert_from_utc(self.asi8, self.tz, reso=self._reso)
