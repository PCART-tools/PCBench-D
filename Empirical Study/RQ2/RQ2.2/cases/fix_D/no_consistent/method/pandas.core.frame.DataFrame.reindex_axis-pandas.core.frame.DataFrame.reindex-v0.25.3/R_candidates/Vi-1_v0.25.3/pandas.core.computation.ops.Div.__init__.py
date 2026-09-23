    def __init__(self, lhs, rhs, truediv, *args, **kwargs):
        super().__init__("/", lhs, rhs, *args, **kwargs)

        if not isnumeric(lhs.return_type) or not isnumeric(rhs.return_type):
            raise TypeError(
                "unsupported operand type(s) for {0}:"
                " '{1}' and '{2}'".format(self.op, lhs.return_type, rhs.return_type)
            )

        # do not upcast float32s to float64 un-necessarily
        acceptable_dtypes = [np.float32, np.float_]
        _cast_inplace(com.flatten(self), acceptable_dtypes, np.float_)
