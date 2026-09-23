    def __new__(
        cls,
        data,
        closed=None,
        dtype=None,
        copy: bool = False,
        verify_integrity: bool = True,
    ):

        if isinstance(data, ABCSeries) and is_interval_dtype(data.dtype):
            data = data._values

        if isinstance(data, (cls, ABCIntervalIndex)):
            left = data.left
            right = data.right
            closed = closed or data.closed
        else:

            # don't allow scalars
            if is_scalar(data):
                msg = (
                    f"{cls.__name__}(...) must be called with a collection "
                    f"of some kind, {data} was passed"
                )
                raise TypeError(msg)

            # might need to convert empty or purely na data
            data = maybe_convert_platform_interval(data)
            left, right, infer_closed = intervals_to_interval_bounds(
                data, validate_closed=closed is None
            )
            closed = closed or infer_closed

        return cls._simple_new(
            left,
            right,
            closed,
            copy=copy,
            dtype=dtype,
            verify_integrity=verify_integrity,
        )
