    @classmethod
    def get_op(cls, left, right, name, na_op):
        """
        Get op dispatcher, returns _Op or _TimeOp.

        If ``left`` and ``right`` are appropriate for datetime arithmetic with
        operation ``name``, processes them and returns a ``_TimeOp`` object
        that stores all the required values.  Otherwise, it will generate
        either a ``_Op``, indicating that the operation is performed via
        normal numpy path.
        """
        is_timedelta_lhs = is_timedelta64_dtype(left)
        is_datetime_lhs = (is_datetime64_dtype(left) or
                           is_datetime64tz_dtype(left))

        if not (is_datetime_lhs or is_timedelta_lhs):
            return _Op(left, right, name, na_op)
        else:
            return _TimeOp(left, right, name, na_op)
