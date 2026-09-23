    def __new__(cls, start=None, stop=None, step=None,
                dtype=None, copy=False, name=None, fastpath=None):

        if fastpath is not None:
            warnings.warn("The 'fastpath' keyword is deprecated, and will be "
                          "removed in a future version.",
                          FutureWarning, stacklevel=2)
            if fastpath:
                return cls._simple_new(start, stop, step, name=name)

        cls._validate_dtype(dtype)

        # RangeIndex
        if isinstance(start, RangeIndex):
            if name is None:
                name = start.name
            return cls._simple_new(name=name,
                                   **dict(start._get_data_as_items()))

        # validate the arguments
        def ensure_int(value, field):
            msg = ("RangeIndex(...) must be called with integers,"
                   " {value} was passed for {field}")
            if not is_scalar(value):
                raise TypeError(msg.format(value=type(value).__name__,
                                           field=field))
            try:
                new_value = int(value)
                assert(new_value == value)
            except (TypeError, ValueError, AssertionError):
                raise TypeError(msg.format(value=type(value).__name__,
                                           field=field))

            return new_value

        if com._all_none(start, stop, step):
            msg = "RangeIndex(...) must be called with integers"
            raise TypeError(msg)
        elif start is None:
            start = 0
        else:
            start = ensure_int(start, 'start')
        if stop is None:
            stop = start
            start = 0
        else:
            stop = ensure_int(stop, 'stop')
        if step is None:
            step = 1
        elif step == 0:
            raise ValueError("Step must not be zero")
        else:
            step = ensure_int(step, 'step')

        return cls._simple_new(start, stop, step, name)
