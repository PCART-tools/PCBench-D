    def __init__(self, values, placement, ndim=2, **kwargs):

        if not isinstance(values, self._holder):
            values = self._holder(values)

        dtype = kwargs.pop('dtype', None)

        if dtype is not None:
            if isinstance(dtype, compat.string_types):
                dtype = DatetimeTZDtype.construct_from_string(dtype)
            values = values._shallow_copy(tz=dtype.tz)

        if values.tz is None:
            raise ValueError("cannot create a DatetimeTZBlock without a tz")

        super(DatetimeTZBlock, self).__init__(values, placement=placement,
                                              ndim=ndim, **kwargs)
