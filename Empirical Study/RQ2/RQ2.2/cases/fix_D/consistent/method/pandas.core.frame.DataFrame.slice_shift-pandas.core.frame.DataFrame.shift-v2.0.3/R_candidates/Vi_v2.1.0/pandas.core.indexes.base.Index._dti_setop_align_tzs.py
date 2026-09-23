    @final
    def _dti_setop_align_tzs(self, other: Index, setop: str_t) -> tuple[Index, Index]:
        """
        With mismatched timezones, cast both to UTC.
        """
        # Caller is responsibelf or checking
        #  `self.dtype != other.dtype`
        if (
            isinstance(self, ABCDatetimeIndex)
            and isinstance(other, ABCDatetimeIndex)
            and self.tz is not None
            and other.tz is not None
        ):
            # GH#39328, GH#45357
            left = self.tz_convert("UTC")
            right = other.tz_convert("UTC")
            return left, right
        return self, other
