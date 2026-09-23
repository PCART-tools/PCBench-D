    def __init__(self, unit: str_type | DatetimeTZDtype = "ns", tz=None) -> None:
        if isinstance(unit, DatetimeTZDtype):
            # error: "str" has no attribute "tz"
            unit, tz = unit.unit, unit.tz  # type: ignore[attr-defined]

        if unit != "ns":
            if isinstance(unit, str) and tz is None:
                # maybe a string like datetime64[ns, tz], which we support for
                # now.
                result = type(self).construct_from_string(unit)
                unit = result.unit
                tz = result.tz
                msg = (
                    f"Passing a dtype alias like 'datetime64[ns, {tz}]' "
                    "to DatetimeTZDtype is no longer supported. Use "
                    "'DatetimeTZDtype.construct_from_string()' instead."
                )
                raise ValueError(msg)
            if unit not in ["s", "ms", "us", "ns"]:
                raise ValueError("DatetimeTZDtype only supports s, ms, us, ns units")

        if tz:
            tz = timezones.maybe_get_tz(tz)
            tz = timezones.tz_standardize(tz)
        elif tz is not None:
            raise pytz.UnknownTimeZoneError(tz)
        if tz is None:
            raise TypeError("A 'tz' is required.")

        self._unit = unit
        self._tz = tz
