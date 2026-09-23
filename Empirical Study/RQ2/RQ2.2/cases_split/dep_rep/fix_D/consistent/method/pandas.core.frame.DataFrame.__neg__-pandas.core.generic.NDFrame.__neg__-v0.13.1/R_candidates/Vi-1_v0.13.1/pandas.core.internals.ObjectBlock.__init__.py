    def __init__(self, values, items, ref_items, ndim=2, fastpath=False,
                 placement=None):
        if issubclass(values.dtype.type, compat.string_types):
            values = np.array(values, dtype=object)

        super(ObjectBlock, self).__init__(values, items, ref_items, ndim=ndim,
                                          fastpath=fastpath,
                                          placement=placement)
