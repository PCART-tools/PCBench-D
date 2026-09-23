    def __init__(self, values, copy=False):
        if isinstance(values, type(self)):
            values = values._ndarray
        if not isinstance(values, np.ndarray):
            raise ValueError("'values' must be a NumPy array.")

        if values.ndim != 1:
            raise ValueError("PandasArray must be 1-dimensional.")

        if copy:
            values = values.copy()

        self._ndarray = values
        self._dtype = PandasDtype(values.dtype)
