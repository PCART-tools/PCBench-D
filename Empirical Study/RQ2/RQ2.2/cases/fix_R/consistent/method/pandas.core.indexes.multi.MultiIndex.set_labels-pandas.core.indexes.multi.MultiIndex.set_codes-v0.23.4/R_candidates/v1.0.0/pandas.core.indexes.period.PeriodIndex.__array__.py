    def __array__(self, dtype=None) -> np.ndarray:
        if is_integer_dtype(dtype):
            return self.asi8
        else:
            return self.astype(object).values
