    def __init__(self, values: np.ndarray, mask: np.ndarray, copy: bool = False):
        if not (isinstance(values, np.ndarray) and values.dtype.kind in ["i", "u"]):
            raise TypeError(
                "values should be integer numpy array. Use "
                "the 'pd.array' function instead"
            )
        super().__init__(values, mask, copy=copy)
