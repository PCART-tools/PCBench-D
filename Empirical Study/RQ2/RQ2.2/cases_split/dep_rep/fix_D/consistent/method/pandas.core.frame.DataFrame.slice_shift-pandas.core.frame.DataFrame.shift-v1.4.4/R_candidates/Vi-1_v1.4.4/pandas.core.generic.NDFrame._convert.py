    @final
    def _convert(
        self: NDFrameT,
        datetime: bool_t = False,
        numeric: bool_t = False,
        timedelta: bool_t = False,
    ) -> NDFrameT:
        """
        Attempt to infer better dtype for object columns.

        Parameters
        ----------
        datetime : bool, default False
            If True, convert to date where possible.
        numeric : bool, default False
            If True, attempt to convert to numbers (including strings), with
            unconvertible values becoming NaN.
        timedelta : bool, default False
            If True, convert to timedelta where possible.

        Returns
        -------
        converted : same as input object
        """
        validate_bool_kwarg(datetime, "datetime")
        validate_bool_kwarg(numeric, "numeric")
        validate_bool_kwarg(timedelta, "timedelta")
        return self._constructor(
            self._mgr.convert(
                datetime=datetime,
                numeric=numeric,
                timedelta=timedelta,
                copy=True,
            )
        ).__finalize__(self)
