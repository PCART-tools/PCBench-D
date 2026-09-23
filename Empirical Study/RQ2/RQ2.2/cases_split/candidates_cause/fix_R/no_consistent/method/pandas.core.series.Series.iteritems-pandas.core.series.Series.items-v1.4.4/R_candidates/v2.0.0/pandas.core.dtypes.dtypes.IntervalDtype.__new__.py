    def __new__(cls, subtype=None, closed: str_type | None = None):
        from pandas.core.dtypes.common import (
            is_string_dtype,
            pandas_dtype,
        )

        if closed is not None and closed not in {"right", "left", "both", "neither"}:
            raise ValueError("closed must be one of 'right', 'left', 'both', 'neither'")

        if isinstance(subtype, IntervalDtype):
            if closed is not None and closed != subtype.closed:
                raise ValueError(
                    "dtype.closed and 'closed' do not match. "
                    "Try IntervalDtype(dtype.subtype, closed) instead."
                )
            return subtype
        elif subtype is None:
            # we are called as an empty constructor
            # generally for pickle compat
            u = object.__new__(cls)
            u._subtype = None
            u._closed = closed
            return u
        elif isinstance(subtype, str) and subtype.lower() == "interval":
            subtype = None
        else:
            if isinstance(subtype, str):
                m = cls._match.search(subtype)
                if m is not None:
                    gd = m.groupdict()
                    subtype = gd["subtype"]
                    if gd.get("closed", None) is not None:
                        if closed is not None:
                            if closed != gd["closed"]:
                                raise ValueError(
                                    "'closed' keyword does not match value "
                                    "specified in dtype string"
                                )
                        closed = gd["closed"]

            try:
                subtype = pandas_dtype(subtype)
            except TypeError as err:
                raise TypeError("could not construct IntervalDtype") from err

        if CategoricalDtype.is_dtype(subtype) or is_string_dtype(subtype):
            # GH 19016
            msg = (
                "category, object, and string subtypes are not supported "
                "for IntervalDtype"
            )
            raise TypeError(msg)

        key = f"{subtype}{closed}"
        try:
            return cls._cache_dtypes[key]
        except KeyError:
            u = object.__new__(cls)
            u._subtype = subtype
            u._closed = closed
            cls._cache_dtypes[key] = u
            return u
