    def __init__(self, values, items, ref_items, fastpath=False,
                 placement=None, **kwargs):
        if values.dtype != _NS_DTYPE:
            values = tslib.cast_to_nanoseconds(values)

        super(DatetimeBlock, self).__init__(values, items, ref_items,
                                            fastpath=True, placement=placement,
                                            **kwargs)
