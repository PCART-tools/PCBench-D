    def __new__(cls, subtype=None):
        """
        Parameters
        ----------
        subtype : the dtype of the Interval
        """
        from pandas.core.dtypes.common import (
            is_categorical_dtype, is_string_dtype, pandas_dtype)

        if isinstance(subtype, IntervalDtype):
            return subtype
        elif subtype is None:
            # we are called as an empty constructor
            # generally for pickle compat
            u = object.__new__(cls)
            u.subtype = None
            return u
        elif (isinstance(subtype, compat.string_types) and
              subtype.lower() == 'interval'):
            subtype = None
        else:
            if isinstance(subtype, compat.string_types):
                m = cls._match.search(subtype)
                if m is not None:
                    subtype = m.group('subtype')

            try:
                subtype = pandas_dtype(subtype)
            except TypeError:
                raise TypeError("could not construct IntervalDtype")

        if is_categorical_dtype(subtype) or is_string_dtype(subtype):
            # GH 19016
            msg = ('category, object, and string subtypes are not supported '
                   'for IntervalDtype')
            raise TypeError(msg)

        try:
            return cls._cache[str(subtype)]
        except KeyError:
            u = object.__new__(cls)
            u.subtype = subtype
            cls._cache[str(subtype)] = u
            return u
