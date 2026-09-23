    def __init__(self, subtype=None, closed: IntervalClosedType | None = None) -> None:
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
            self._subtype = subtype._subtype
            self._closed = subtype._closed
        elif subtype is None:
            # we are called as an empty constructor
            # generally for pickle compat
            self._subtype = None
            self._closed = closed
        elif isinstance(subtype, str) and subtype.lower() == "interval":
            self._subtype = None
            self._closed = closed
        else:
            if isinstance(subtype, str):
                m = IntervalDtype._match.search(subtype)
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
                        closed = gd["closed"]  # type: ignore[assignment]

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
            self._subtype = subtype
            self._closed = closed
