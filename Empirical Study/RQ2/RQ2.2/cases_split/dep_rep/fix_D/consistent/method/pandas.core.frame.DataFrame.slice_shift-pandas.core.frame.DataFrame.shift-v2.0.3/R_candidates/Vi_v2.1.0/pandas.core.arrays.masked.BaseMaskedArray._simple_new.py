    @classmethod
    def _simple_new(cls, values: np.ndarray, mask: npt.NDArray[np.bool_]) -> Self:
        result = BaseMaskedArray.__new__(cls)
        result._data = values
        result._mask = mask
        return result
