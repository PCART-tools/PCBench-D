    def __init__(self, left, right, name, na_op):
        super(_TimeOp, self).__init__(left, right, name, na_op)

        lvalues = self._convert_to_array(left, name=name)
        rvalues = self._convert_to_array(right, name=name, other=lvalues)

        # left
        self.is_offset_lhs = self._is_offset(left)
        self.is_timedelta_lhs = is_timedelta64_dtype(lvalues)
        self.is_datetime64_lhs = is_datetime64_dtype(lvalues)
        self.is_datetime64tz_lhs = is_datetime64tz_dtype(lvalues)
        self.is_datetime_lhs = (self.is_datetime64_lhs or
                                self.is_datetime64tz_lhs)
        self.is_integer_lhs = left.dtype.kind in ['i', 'u']
        self.is_floating_lhs = left.dtype.kind == 'f'

        # right
        self.is_offset_rhs = self._is_offset(right)
        self.is_datetime64_rhs = is_datetime64_dtype(rvalues)
        self.is_datetime64tz_rhs = is_datetime64tz_dtype(rvalues)
        self.is_datetime_rhs = (self.is_datetime64_rhs or
                                self.is_datetime64tz_rhs)
        self.is_timedelta_rhs = is_timedelta64_dtype(rvalues)
        self.is_integer_rhs = rvalues.dtype.kind in ('i', 'u')
        self.is_floating_rhs = rvalues.dtype.kind == 'f'

        self._validate(lvalues, rvalues, name)
        self.lvalues, self.rvalues = self._convert_for_datetime(lvalues,
                                                                rvalues)
