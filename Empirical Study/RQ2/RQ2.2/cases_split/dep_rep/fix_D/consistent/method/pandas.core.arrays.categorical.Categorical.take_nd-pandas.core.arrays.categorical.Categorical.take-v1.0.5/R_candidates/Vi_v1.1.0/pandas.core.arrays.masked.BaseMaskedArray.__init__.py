    def __init__(self, values: np.ndarray, mask: np.ndarray, copy: bool = False):
        # values is supposed to already be validated in the subclass
        if not (isinstance(mask, np.ndarray) and mask.dtype == np.bool_):
            raise TypeError(
                "mask should be boolean numpy array. Use "
                "the 'pd.array' function instead"
            )
        if not values.ndim == 1:
            raise ValueError("values must be a 1D array")
        if not mask.ndim == 1:
            raise ValueError("mask must be a 1D array")

        if copy:
            values = values.copy()
            mask = mask.copy()

        self._data = values
        self._mask = mask
