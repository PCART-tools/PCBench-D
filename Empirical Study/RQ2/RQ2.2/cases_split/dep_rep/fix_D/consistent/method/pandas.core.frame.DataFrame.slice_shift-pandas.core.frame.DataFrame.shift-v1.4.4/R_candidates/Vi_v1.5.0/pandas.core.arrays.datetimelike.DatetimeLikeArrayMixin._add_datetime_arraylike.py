    @final
    def _add_datetime_arraylike(self, other) -> DatetimeArray:
        if not is_timedelta64_dtype(self.dtype):
            raise TypeError(
                f"cannot add {type(self).__name__} and {type(other).__name__}"
            )

        # At this point we have already checked that other.dtype is datetime64
        other = ensure_wrapped_if_datetimelike(other)
        # defer to DatetimeArray.__add__
        return other + self
