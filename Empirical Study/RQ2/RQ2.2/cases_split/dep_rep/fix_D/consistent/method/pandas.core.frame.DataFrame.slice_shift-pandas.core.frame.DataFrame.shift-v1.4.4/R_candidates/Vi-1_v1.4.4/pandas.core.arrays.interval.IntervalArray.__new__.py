    def __new__(
        cls: type[IntervalArrayT],
        data,
        closed=None,
        dtype: Dtype | None = None,
        copy: bool = False,
        verify_integrity: bool = True,
    ):

        data = extract_array(data, extract_numpy=True)

        if isinstance(data, cls):
            left = data._left
            right = data._right
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
            data = _maybe_convert_platform_interval(data)
            left, right, infer_closed = intervals_to_interval_bounds(
                data, validate_closed=closed is None
            )
            if left.dtype == object:
                left = lib.maybe_convert_objects(left)
                right = lib.maybe_convert_objects(right)
            closed = closed or infer_closed

        return cls._simple_new(
            left,
            right,
            closed,
            copy=copy,
            dtype=dtype,
            verify_integrity=verify_integrity,
        )
