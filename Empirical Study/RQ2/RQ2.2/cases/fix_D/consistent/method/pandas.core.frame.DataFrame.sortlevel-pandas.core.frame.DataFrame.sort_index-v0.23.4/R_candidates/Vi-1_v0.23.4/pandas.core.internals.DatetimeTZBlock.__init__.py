    def __init__(self, values, placement, ndim=2, dtype=None):
        # XXX: This will end up calling _maybe_coerce_values twice
        # when dtype is not None. It's relatively cheap (just an isinstance)
        # but it'd nice to avoid.
        #
        # If we can remove dtype from __init__, and push that conversion
        # push onto the callers, then we can remove this entire __init__
        # and just use DatetimeBlock's.
        if dtype is not None:
            values = self._maybe_coerce_values(values, dtype=dtype)
        super(DatetimeTZBlock, self).__init__(values, placement=placement,
                                              ndim=ndim)
