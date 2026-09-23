    def _maybe_utc_convert(self, other):
        this = self
        if isinstance(other, DatetimeIndex):
            if self.tz is not None:
                if other.tz is None:
                    raise TypeError(
                        "Cannot join tz-naive with tz-aware " "DatetimeIndex"
                    )
            elif other.tz is not None:
                raise TypeError("Cannot join tz-naive with tz-aware " "DatetimeIndex")

            if not timezones.tz_compare(self.tz, other.tz):
                this = self.tz_convert("UTC")
                other = other.tz_convert("UTC")
        return this, other
