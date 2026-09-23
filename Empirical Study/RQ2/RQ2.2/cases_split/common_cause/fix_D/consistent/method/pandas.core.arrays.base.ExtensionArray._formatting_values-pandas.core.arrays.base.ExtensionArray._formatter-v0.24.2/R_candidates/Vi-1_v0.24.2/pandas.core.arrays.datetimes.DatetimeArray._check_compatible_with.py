    def _check_compatible_with(self, other):
        if other is NaT:
            return
        if not timezones.tz_compare(self.tz, other.tz):
            raise ValueError("Timezones don't match. '{own} != {other}'"
                             .format(own=self.tz, other=other.tz))
