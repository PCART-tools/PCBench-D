    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            if other.startswith("M8["):
                other = "datetime64[" + other[3:]
            return other == self.name

        return (
            isinstance(other, DatetimeTZDtype)
            and self.unit == other.unit
            and tz_compare(self.tz, other.tz)
        )
