    def __init__(self, values, placement=None, ndim=2):
        if issubclass(values.dtype.type, str):
            values = np.array(values, dtype=object)

        super().__init__(values, ndim=ndim, placement=placement)
