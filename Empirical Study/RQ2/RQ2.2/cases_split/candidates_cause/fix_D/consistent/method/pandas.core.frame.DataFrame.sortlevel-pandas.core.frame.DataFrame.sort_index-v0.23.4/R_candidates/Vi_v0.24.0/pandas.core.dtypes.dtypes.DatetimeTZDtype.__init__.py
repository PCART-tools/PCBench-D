    def __init__(self, unit="ns", tz=None):
        """
        An ExtensionDtype for timezone-aware datetime data.

        Parameters
        ----------
        unit : str, default "ns"
            The precision of the datetime data. Currently limited
            to ``"ns"``.
        tz : str, int, or datetime.tzinfo
            The timezone.

        Raises
        ------
        pytz.UnknownTimeZoneError
            When the requested timezone cannot be found.

        Examples
        --------
        >>> pd.core.dtypes.dtypes.DatetimeTZDtype(tz='UTC')
        datetime64[ns, UTC]

        >>> pd.core.dtypes.dtypes.DatetimeTZDtype(tz='dateutil/US/Central')
        datetime64[ns, tzfile('/usr/share/zoneinfo/US/Central')]
        """
        if isinstance(unit, DatetimeTZDtype):
            unit, tz = unit.unit, unit.tz

        if unit != 'ns':
            if isinstance(unit, compat.string_types) and tz is None:
                # maybe a string like datetime64[ns, tz], which we support for
                # now.
                result = type(self).construct_from_string(unit)
                unit = result.unit
                tz = result.tz
                msg = (
                    "Passing a dtype alias like 'datetime64[ns, {tz}]' "
                    "to DatetimeTZDtype is deprecated. Use "
                    "'DatetimeTZDtype.construct_from_string()' instead."
                )
                warnings.warn(msg.format(tz=tz), FutureWarning, stacklevel=2)
            else:
                raise ValueError("DatetimeTZDtype only supports ns units")

        if tz:
            tz = timezones.maybe_get_tz(tz)
        elif tz is not None:
            raise pytz.UnknownTimeZoneError(tz)
        elif tz is None:
            raise TypeError("A 'tz' is required.")

        self._unit = unit
        self._tz = tz
