    @final
    def _add_datetime_arraylike(self, other: DatetimeArray) -> DatetimeArray:
        if not lib.is_np_dtype(self.dtype, "m"):
            raise TypeError(
                f"cannot add {type(self).__name__} and {type(other).__name__}"
            )

        # defer to DatetimeArray.__add__
        return other + self
