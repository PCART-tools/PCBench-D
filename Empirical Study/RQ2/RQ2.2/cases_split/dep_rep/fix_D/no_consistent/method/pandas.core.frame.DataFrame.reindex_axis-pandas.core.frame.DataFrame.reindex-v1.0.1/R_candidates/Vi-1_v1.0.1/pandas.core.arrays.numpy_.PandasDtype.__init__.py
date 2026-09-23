    def __init__(self, dtype):
        dtype = np.dtype(dtype)
        self._dtype = dtype
        self._type = dtype.type
