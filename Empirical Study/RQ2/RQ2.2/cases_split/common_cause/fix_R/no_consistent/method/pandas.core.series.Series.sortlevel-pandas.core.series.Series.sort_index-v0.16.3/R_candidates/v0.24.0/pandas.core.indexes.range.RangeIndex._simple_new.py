    @classmethod
    def _simple_new(cls, start, stop=None, step=None, name=None,
                    dtype=None, **kwargs):
        result = object.__new__(cls)

        # handle passed None, non-integers
        if start is None and stop is None:
            # empty
            start, stop, step = 0, 0, 1

        if start is None or not is_integer(start):
            try:

                return RangeIndex(start, stop, step, name=name, **kwargs)
            except TypeError:
                return Index(start, stop, step, name=name, **kwargs)

        result._start = start
        result._stop = stop or 0
        result._step = step or 1
        result.name = name
        for k, v in compat.iteritems(kwargs):
            setattr(result, k, v)

        result._reset_identity()
        return result
