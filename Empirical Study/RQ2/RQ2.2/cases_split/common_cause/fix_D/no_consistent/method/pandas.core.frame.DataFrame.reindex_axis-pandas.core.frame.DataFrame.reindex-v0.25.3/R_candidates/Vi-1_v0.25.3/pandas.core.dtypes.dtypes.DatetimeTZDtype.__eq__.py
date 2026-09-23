    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.name

        return (
            isinstance(other, DatetimeTZDtype)
            and self.unit == other.unit
            and str(self.tz) == str(other.tz)
        )
