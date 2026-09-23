    def __init__(self, lhs, rhs):
        super().__init__("/", lhs, rhs)

        if not isnumeric(lhs.return_type) or not isnumeric(rhs.return_type):
            raise TypeError(
                f"unsupported operand type(s) for {self.op}: "
                f"'{lhs.return_type}' and '{rhs.return_type}'"
            )

        # do not upcast float32s to float64 un-necessarily
        acceptable_dtypes = [np.float32, np.float_]
        _cast_inplace(com.flatten(self), acceptable_dtypes, np.float_)
