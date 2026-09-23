    @classmethod
    def maybe_convert_for_time_op(cls, left, right, name):
        """
        if ``left`` and ``right`` are appropriate for datetime arithmetic with
        operation ``name``, processes them and returns a ``_TimeOp`` object
        that stores all the required values.  Otherwise, it will generate
        either a ``NotImplementedError`` or ``None``, indicating that the
        operation is unsupported for datetimes (e.g., an unsupported r_op) or
        that the data is not the right type for time ops.
        """
        # decide if we can do it
        is_timedelta_lhs = com.is_timedelta64_dtype(left)
        is_datetime_lhs = com.is_datetime64_dtype(left)
        if not (is_datetime_lhs or is_timedelta_lhs):
            return None
        # rops are allowed. No need for special checks, just strip off
        # r part.
        if name.startswith('__r'):
            name = "__" + name[3:]
        return cls(left, right, name)
