    @classmethod
    def _simple_new(
        cls, left, right, closed=None, copy=False, dtype=None, verify_integrity=True
    ):
        result = IntervalMixin.__new__(cls)

        closed = closed or "right"
        left = ensure_index(left, copy=copy)
        right = ensure_index(right, copy=copy)

        if dtype is not None:
            # GH 19262: dtype must be an IntervalDtype to override inferred
            dtype = pandas_dtype(dtype)
            if not is_interval_dtype(dtype):
                msg = "dtype must be an IntervalDtype, got {dtype}"
                raise TypeError(msg.format(dtype=dtype))
            elif dtype.subtype is not None:
                left = left.astype(dtype.subtype)
                right = right.astype(dtype.subtype)

        # coerce dtypes to match if needed
        if is_float_dtype(left) and is_integer_dtype(right):
            right = right.astype(left.dtype)
        elif is_float_dtype(right) and is_integer_dtype(left):
            left = left.astype(right.dtype)

        if type(left) != type(right):
            msg = "must not have differing left [{ltype}] and right " "[{rtype}] types"
            raise ValueError(
                msg.format(ltype=type(left).__name__, rtype=type(right).__name__)
            )
        elif is_categorical_dtype(left.dtype) or is_string_dtype(left.dtype):
            # GH 19016
            msg = (
                "category, object, and string subtypes are not supported "
                "for IntervalArray"
            )
            raise TypeError(msg)
        elif isinstance(left, ABCPeriodIndex):
            msg = "Period dtypes are not supported, use a PeriodIndex instead"
            raise ValueError(msg)
        elif isinstance(left, ABCDatetimeIndex) and str(left.tz) != str(right.tz):
            msg = (
                "left and right must have the same time zone, got "
                "'{left_tz}' and '{right_tz}'"
            )
            raise ValueError(msg.format(left_tz=left.tz, right_tz=right.tz))

        result._left = left
        result._right = right
        result._closed = closed
        if verify_integrity:
            result._validate()
        return result
