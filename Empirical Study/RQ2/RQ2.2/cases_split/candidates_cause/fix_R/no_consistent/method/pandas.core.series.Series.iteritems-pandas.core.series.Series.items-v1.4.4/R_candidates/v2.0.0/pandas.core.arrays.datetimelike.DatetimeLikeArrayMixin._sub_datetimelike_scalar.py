    @final
    def _sub_datetimelike_scalar(self, other: datetime | np.datetime64):
        if self.dtype.kind != "M":
            raise TypeError(f"cannot subtract a datelike from a {type(self).__name__}")

        self = cast("DatetimeArray", self)
        # subtract a datetime from myself, yielding a ndarray[timedelta64[ns]]

        if isna(other):
            # i.e. np.datetime64("NaT")
            return self - NaT

        ts = Timestamp(other)

        self, ts = self._ensure_matching_resos(ts)
        return self._sub_datetimelike(ts)
