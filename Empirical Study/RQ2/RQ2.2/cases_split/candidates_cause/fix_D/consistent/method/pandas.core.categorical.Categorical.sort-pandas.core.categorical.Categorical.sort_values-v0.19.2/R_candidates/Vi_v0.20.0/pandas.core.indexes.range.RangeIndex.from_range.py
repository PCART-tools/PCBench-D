    @classmethod
    def from_range(cls, data, name=None, dtype=None, **kwargs):
        """ create RangeIndex from a range (py3), or xrange (py2) object """
        if not isinstance(data, range):
            raise TypeError(
                '{0}(...) must be called with object coercible to a '
                'range, {1} was passed'.format(cls.__name__, repr(data)))

        if compat.PY3:
            step = data.step
            stop = data.stop
            start = data.start
        else:
            # seems we only have indexing ops to infer
            # rather than direct accessors
            if len(data) > 1:
                step = data[1] - data[0]
                stop = data[-1] + step
                start = data[0]
            elif len(data):
                start = data[0]
                stop = data[0] + 1
                step = 1
            else:
                start = stop = 0
                step = 1
        return RangeIndex(start, stop, step, dtype=dtype, name=name, **kwargs)
