    @classmethod
    def construct_from_string(cls, string: str_type) -> DatetimeTZDtype:
        """
        Construct a DatetimeTZDtype from a string.

        Parameters
        ----------
        string : str
            The string alias for this DatetimeTZDtype.
            Should be formatted like ``datetime64[ns, <tz>]``,
            where ``<tz>`` is the timezone name.

        Examples
        --------
        >>> DatetimeTZDtype.construct_from_string('datetime64[ns, UTC]')
        datetime64[ns, UTC]
        """
        if not isinstance(string, str):
            raise TypeError(
                f"'construct_from_string' expects a string, got {type(string)}"
            )

        msg = f"Cannot construct a 'DatetimeTZDtype' from '{string}'"
        match = cls._match.match(string)
        if match:
            d = match.groupdict()
            try:
                return cls(unit=d["unit"], tz=d["tz"])
            except (KeyError, TypeError, ValueError) as err:
                # KeyError if maybe_get_tz tries and fails to get a
                #  pytz timezone (actually pytz.UnknownTimeZoneError).
                # TypeError if we pass a nonsense tz;
                # ValueError if we pass a unit other than "ns"
                raise TypeError(msg) from err
        raise TypeError(msg)
