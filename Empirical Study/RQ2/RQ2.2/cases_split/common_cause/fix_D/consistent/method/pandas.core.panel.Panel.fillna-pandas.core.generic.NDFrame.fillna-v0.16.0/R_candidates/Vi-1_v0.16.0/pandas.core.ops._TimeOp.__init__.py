    def __init__(self, left, right, name):
        self.name = name

        # need to make sure that we are aligning the data
        if isinstance(left, pd.Series) and isinstance(right, pd.Series):
            left, right = left.align(right,copy=False)

        self.left = left
        self.right = right
        lvalues = self._convert_to_array(left, name=name)
        rvalues = self._convert_to_array(right, name=name, other=lvalues)

        self.is_timedelta_lhs = com.is_timedelta64_dtype(left)
        self.is_datetime_lhs = com.is_datetime64_dtype(left)
        self.is_integer_lhs = left.dtype.kind in ['i', 'u']
        self.is_datetime_rhs = com.is_datetime64_dtype(rvalues)
        self.is_timedelta_rhs = com.is_timedelta64_dtype(rvalues)
        self.is_integer_rhs = rvalues.dtype.kind in ('i', 'u')

        self._validate()

        self._convert_for_datetime(lvalues, rvalues)
