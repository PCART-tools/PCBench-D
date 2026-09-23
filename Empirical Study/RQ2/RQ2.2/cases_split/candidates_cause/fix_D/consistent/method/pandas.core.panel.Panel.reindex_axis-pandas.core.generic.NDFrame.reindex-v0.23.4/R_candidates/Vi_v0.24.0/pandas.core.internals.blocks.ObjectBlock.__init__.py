    def __init__(self, values, placement=None, ndim=2):
        if issubclass(values.dtype.type, compat.string_types):
            values = np.array(values, dtype=object)

        super(ObjectBlock, self).__init__(values, ndim=ndim,
                                          placement=placement)
