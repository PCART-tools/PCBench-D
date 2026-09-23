    @classmethod
    def from_range(cls, data, name=None, dtype=None, **kwargs):
        """ create RangeIndex from a range (py3), or xrange (py2) object """
        if not isinstance(data, range):
            raise TypeError(
                '{0}(...) must be called with object coercible to a '
                'range, {1} was passed'.format(cls.__name__, repr(data)))

        start, stop, step = get_range_parameters(data)
        return RangeIndex(start, stop, step, dtype=dtype, name=name, **kwargs)
