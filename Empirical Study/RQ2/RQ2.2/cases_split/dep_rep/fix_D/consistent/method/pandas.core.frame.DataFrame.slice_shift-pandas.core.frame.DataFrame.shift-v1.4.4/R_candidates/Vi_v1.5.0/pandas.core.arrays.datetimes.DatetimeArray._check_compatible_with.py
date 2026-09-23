    def _check_compatible_with(self, other, setitem: bool = False):
        if other is NaT:
            return
        self._assert_tzawareness_compat(other)
        if setitem:
            # Stricter check for setitem vs comparison methods
            if self.tz is not None and not timezones.tz_compare(self.tz, other.tz):
                # TODO(2.0): remove this check. GH#37605
                warnings.warn(
                    "Setitem-like behavior with mismatched timezones is deprecated "
                    "and will change in a future version. Instead of raising "
                    "(or for Index, Series, and DataFrame methods, coercing to "
                    "object dtype), the value being set (or passed as a "
                    "fill_value, or inserted) will be cast to the existing "
                    "DatetimeArray/DatetimeIndex/Series/DataFrame column's "
                    "timezone. To retain the old behavior, explicitly cast to "
                    "object dtype before the operation.",
                    FutureWarning,
                    stacklevel=find_stack_level(inspect.currentframe()),
                )
                raise ValueError(f"Timezones don't match. '{self.tz}' != '{other.tz}'")
