    @classmethod
    def construct_from_string(cls, string):
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
        if isinstance(string, compat.string_types):
            msg = "Could not construct DatetimeTZDtype from '{}'"
            try:
                match = cls._match.match(string)
                if match:
                    d = match.groupdict()
                    return cls(unit=d['unit'], tz=d['tz'])
            except Exception:
                # TODO(py3): Change this pass to `raise TypeError(msg) from e`
                pass
            raise TypeError(msg.format(string))

        raise TypeError("Could not construct DatetimeTZDtype")
