    def __init__(self, dtype):
        dtype = np.dtype(dtype)
        self._dtype = dtype
        self._name = dtype.name
        self._type = dtype.type
