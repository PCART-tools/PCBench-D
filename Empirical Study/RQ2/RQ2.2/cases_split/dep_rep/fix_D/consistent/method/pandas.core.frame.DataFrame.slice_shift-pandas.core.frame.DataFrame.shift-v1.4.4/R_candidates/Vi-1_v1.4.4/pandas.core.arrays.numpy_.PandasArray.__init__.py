    def __init__(self, values: np.ndarray | PandasArray, copy: bool = False):
        if isinstance(values, type(self)):
            values = values._ndarray
        if not isinstance(values, np.ndarray):
            raise ValueError(
                f"'values' must be a NumPy array, not {type(values).__name__}"
            )

        if values.ndim == 0:
            # Technically we support 2, but do not advertise that fact.
            raise ValueError("PandasArray must be 1-dimensional.")

        if copy:
            values = values.copy()

        dtype = PandasDtype(values.dtype)
        super().__init__(values, dtype)
