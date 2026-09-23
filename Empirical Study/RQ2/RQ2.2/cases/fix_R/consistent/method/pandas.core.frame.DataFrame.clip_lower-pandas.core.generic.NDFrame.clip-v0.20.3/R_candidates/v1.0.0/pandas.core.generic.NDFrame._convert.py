    def _convert(
        self: FrameOrSeries,
        datetime: bool_t = False,
        numeric: bool_t = False,
        timedelta: bool_t = False,
        coerce: bool_t = False,
        copy: bool_t = True,
    ) -> FrameOrSeries:
        """
        Attempt to infer better dtype for object columns

        Parameters
        ----------
        datetime : bool, default False
            If True, convert to date where possible.
        numeric : bool, default False
            If True, attempt to convert to numbers (including strings), with
            unconvertible values becoming NaN.
        timedelta : bool, default False
            If True, convert to timedelta where possible.
        coerce : bool, default False
            If True, force conversion with unconvertible values converted to
            nulls (NaN or NaT).
        copy : bool, default True
            If True, return a copy even if no copy is necessary (e.g. no
            conversion was done). Note: This is meant for internal use, and
            should not be confused with inplace.

        Returns
        -------
        converted : same as input object
        """
        validate_bool_kwarg(datetime, "datetime")
        validate_bool_kwarg(numeric, "numeric")
        validate_bool_kwarg(timedelta, "timedelta")
        validate_bool_kwarg(coerce, "coerce")
        validate_bool_kwarg(copy, "copy")
        return self._constructor(
            self._data.convert(
                datetime=datetime,
                numeric=numeric,
                timedelta=timedelta,
                coerce=coerce,
                copy=copy,
            )
        ).__finalize__(self)
