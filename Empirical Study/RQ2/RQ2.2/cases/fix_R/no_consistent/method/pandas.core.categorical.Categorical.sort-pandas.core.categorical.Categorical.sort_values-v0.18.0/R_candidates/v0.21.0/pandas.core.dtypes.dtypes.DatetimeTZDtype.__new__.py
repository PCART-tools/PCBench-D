    def __new__(cls, unit=None, tz=None):
        """ Create a new unit if needed, otherwise return from the cache

        Parameters
        ----------
        unit : string unit that this represents, currently must be 'ns'
        tz : string tz that this represents
        """

        if isinstance(unit, DatetimeTZDtype):
            unit, tz = unit.unit, unit.tz

        elif unit is None:
            # we are called as an empty constructor
            # generally for pickle compat
            return object.__new__(cls)

        elif tz is None:

            # we were passed a string that we can construct
            try:
                m = cls._match.search(unit)
                if m is not None:
                    unit = m.groupdict()['unit']
                    tz = m.groupdict()['tz']
            except:
                raise ValueError("could not construct DatetimeTZDtype")

        elif isinstance(unit, compat.string_types):

            if unit != 'ns':
                raise ValueError("DatetimeTZDtype only supports ns units")

            unit = unit
            tz = tz

        if tz is None:
            raise ValueError("DatetimeTZDtype constructor must have a tz "
                             "supplied")

        # hash with the actual tz if we can
        # some cannot be hashed, so stringfy
        try:
            key = (unit, tz)
            hash(key)
        except TypeError:
            key = (unit, str(tz))

        # set/retrieve from cache
        try:
            return cls._cache[key]
        except KeyError:
            u = object.__new__(cls)
            u.unit = unit
            u.tz = tz
            cls._cache[key] = u
            return u
