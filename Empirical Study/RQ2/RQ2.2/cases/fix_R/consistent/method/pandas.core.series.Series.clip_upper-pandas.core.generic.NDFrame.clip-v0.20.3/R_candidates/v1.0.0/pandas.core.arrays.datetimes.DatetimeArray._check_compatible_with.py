    def _check_compatible_with(self, other, setitem: bool = False):
        if other is NaT:
            return
        self._assert_tzawareness_compat(other)
        if setitem:
            # Stricter check for setitem vs comparison methods
            if not timezones.tz_compare(self.tz, other.tz):
                raise ValueError(f"Timezones don't match. '{self.tz} != {other.tz}'")
