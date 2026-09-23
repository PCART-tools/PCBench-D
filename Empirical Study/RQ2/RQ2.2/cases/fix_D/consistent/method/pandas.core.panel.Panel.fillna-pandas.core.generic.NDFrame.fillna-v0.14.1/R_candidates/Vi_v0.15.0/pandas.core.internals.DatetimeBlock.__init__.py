    def __init__(self, values, placement,
                 fastpath=False, **kwargs):
        if values.dtype != _NS_DTYPE:
            values = tslib.cast_to_nanoseconds(values)

        super(DatetimeBlock, self).__init__(values,
                                            fastpath=True, placement=placement,
                                            **kwargs)
