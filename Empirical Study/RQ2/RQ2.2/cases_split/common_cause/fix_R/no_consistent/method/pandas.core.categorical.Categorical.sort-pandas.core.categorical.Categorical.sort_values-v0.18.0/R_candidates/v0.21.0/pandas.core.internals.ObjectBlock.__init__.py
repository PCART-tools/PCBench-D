    def __init__(self, values, ndim=2, fastpath=False, placement=None,
                 **kwargs):
        if issubclass(values.dtype.type, compat.string_types):
            values = np.array(values, dtype=object)

        super(ObjectBlock, self).__init__(values, ndim=ndim, fastpath=fastpath,
                                          placement=placement, **kwargs)
