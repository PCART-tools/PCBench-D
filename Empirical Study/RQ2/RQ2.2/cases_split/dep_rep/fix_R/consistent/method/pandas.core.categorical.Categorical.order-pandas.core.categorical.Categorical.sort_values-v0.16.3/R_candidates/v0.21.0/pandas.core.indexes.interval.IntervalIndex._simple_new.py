    @classmethod
    def _simple_new(cls, left, right, closed=None, name=None,
                    copy=False, verify_integrity=True):
        result = IntervalMixin.__new__(cls)

        if closed is None:
            closed = 'right'
        left = _ensure_index(left, copy=copy)
        right = _ensure_index(right, copy=copy)

        # coerce dtypes to match if needed
        if is_float_dtype(left) and is_integer_dtype(right):
            right = right.astype(left.dtype)
        if is_float_dtype(right) and is_integer_dtype(left):
            left = left.astype(right.dtype)

        if type(left) != type(right):
            raise ValueError("must not have differing left [{}] "
                             "and right [{}] types".format(
                                 type(left), type(right)))

        if isinstance(left, ABCPeriodIndex):
            raise ValueError("Period dtypes are not supported, "
                             "use a PeriodIndex instead")

        result._left = left
        result._right = right
        result._closed = closed
        result.name = name
        if verify_integrity:
            result._validate()
        result._reset_identity()
        return result
