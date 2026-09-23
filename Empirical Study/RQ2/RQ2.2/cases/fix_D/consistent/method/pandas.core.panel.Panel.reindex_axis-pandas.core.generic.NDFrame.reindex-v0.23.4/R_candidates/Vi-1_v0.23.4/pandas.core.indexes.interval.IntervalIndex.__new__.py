    def __new__(cls, data, closed=None, dtype=None, copy=False,
                name=None, fastpath=False, verify_integrity=True):

        if fastpath:
            return cls._simple_new(data.left, data.right, closed, name,
                                   copy=copy, verify_integrity=False)

        if name is None and hasattr(data, 'name'):
            name = data.name

        if isinstance(data, IntervalIndex):
            left = data.left
            right = data.right
            closed = data.closed
        else:

            # don't allow scalars
            if is_scalar(data):
                cls._scalar_data_error(data)

            data = maybe_convert_platform_interval(data)
            left, right, infer_closed = intervals_to_interval_bounds(data)

            if (com._all_not_none(closed, infer_closed) and
                    closed != infer_closed):
                # GH 18421
                msg = ("conflicting values for closed: constructor got "
                       "'{closed}', inferred from data '{infer_closed}'"
                       .format(closed=closed, infer_closed=infer_closed))
                raise ValueError(msg)

            closed = closed or infer_closed

        return cls._simple_new(left, right, closed, name, copy=copy,
                               dtype=dtype, verify_integrity=verify_integrity)
