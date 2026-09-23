    def __array__(self, dtype=None) -> np.ndarray:
        return com.values_from_object(self)
