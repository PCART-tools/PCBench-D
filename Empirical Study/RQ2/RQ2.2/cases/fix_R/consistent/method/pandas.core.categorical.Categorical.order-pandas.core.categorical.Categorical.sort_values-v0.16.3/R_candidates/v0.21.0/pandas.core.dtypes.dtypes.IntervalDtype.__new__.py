    def __new__(cls, subtype=None):
        """
        Parameters
        ----------
        subtype : the dtype of the Interval
        """

        if isinstance(subtype, IntervalDtype):
            return subtype
        elif subtype is None:
            # we are called as an empty constructor
            # generally for pickle compat
            u = object.__new__(cls)
            u.subtype = None
            return u
        elif (isinstance(subtype, compat.string_types) and
              subtype == 'interval'):
            subtype = ''
        else:
            if isinstance(subtype, compat.string_types):
                m = cls._match.search(subtype)
                if m is not None:
                    subtype = m.group('subtype')

            from pandas.core.dtypes.common import pandas_dtype
            try:
                subtype = pandas_dtype(subtype)
            except TypeError:
                raise ValueError("could not construct IntervalDtype")

        if subtype is None:
            u = object.__new__(cls)
            u.subtype = None
            return u

        try:
            return cls._cache[str(subtype)]
        except KeyError:
            u = object.__new__(cls)
            u.subtype = subtype
            cls._cache[str(subtype)] = u
            return u
