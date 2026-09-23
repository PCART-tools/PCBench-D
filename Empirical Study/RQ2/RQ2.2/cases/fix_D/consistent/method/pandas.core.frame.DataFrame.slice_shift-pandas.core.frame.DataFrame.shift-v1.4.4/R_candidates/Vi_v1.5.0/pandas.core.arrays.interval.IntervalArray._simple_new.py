    @classmethod
    def _simple_new(
        cls: type[IntervalArrayT],
        left,
        right,
        closed: IntervalClosedType | None = None,
        copy: bool = False,
        dtype: Dtype | None = None,
        verify_integrity: bool = True,
    ) -> IntervalArrayT:
        result = IntervalMixin.__new__(cls)

        if closed is None and isinstance(dtype, IntervalDtype):
            closed = dtype.closed

        closed = closed or "right"
        left = ensure_index(left, copy=copy)
        right = ensure_index(right, copy=copy)

        if dtype is not None:
            # GH 19262: dtype must be an IntervalDtype to override inferred
            dtype = pandas_dtype(dtype)
            if is_interval_dtype(dtype):
                dtype = cast(IntervalDtype, dtype)
                if dtype.subtype is not None:
                    left = left.astype(dtype.subtype)
                    right = right.astype(dtype.subtype)
            else:
                msg = f"dtype must be an IntervalDtype, got {dtype}"
                raise TypeError(msg)

            if dtype.closed is None:
                # possibly loading an old pickle
                dtype = IntervalDtype(dtype.subtype, closed)
            elif closed != dtype.closed:
                raise ValueError("closed keyword does not match dtype.closed")

        # coerce dtypes to match if needed
        if is_float_dtype(left) and is_integer_dtype(right):
            right = right.astype(left.dtype)
        elif is_float_dtype(right) and is_integer_dtype(left):
            left = left.astype(right.dtype)

        if type(left) != type(right):
            msg = (
                f"must not have differing left [{type(left).__name__}] and "
                f"right [{type(right).__name__}] types"
            )
            raise ValueError(msg)
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
                f"'{left.tz}' and '{right.tz}'"
            )
            raise ValueError(msg)

        # For dt64/td64 we want DatetimeArray/TimedeltaArray instead of ndarray
        left = ensure_wrapped_if_datetimelike(left)
        left = extract_array(left, extract_numpy=True)
        right = ensure_wrapped_if_datetimelike(right)
        right = extract_array(right, extract_numpy=True)

        lbase = getattr(left, "_ndarray", left).base
        rbase = getattr(right, "_ndarray", right).base
        if lbase is not None and lbase is rbase:
            # If these share data, then setitem could corrupt our IA
            right = right.copy()

        dtype = IntervalDtype(left.dtype, closed=closed)
        result._dtype = dtype

        result._left = left
        result._right = right
        if verify_integrity:
            result._validate()
        return result
