    def __init__(self, left, right, name):
        self.name = name

        lvalues = self._convert_to_array(left, name=name)
        rvalues = self._convert_to_array(right, name=name, other=lvalues)

        self.is_timedelta_lhs = com.is_timedelta64_dtype(left)
        self.is_datetime_lhs = com.is_datetime64_dtype(left)
        self.is_integer_lhs = left.dtype.kind in ['i', 'u']
        self.is_datetime_rhs = com.is_datetime64_dtype(rvalues)
        self.is_timedelta_rhs = (com.is_timedelta64_dtype(rvalues)
                                 or (not self.is_datetime_rhs
                                     and pd._np_version_under1p7))
        self.is_integer_rhs = rvalues.dtype.kind in ('i', 'u')

        self._validate()

        self._convert_for_datetime(lvalues, rvalues)
