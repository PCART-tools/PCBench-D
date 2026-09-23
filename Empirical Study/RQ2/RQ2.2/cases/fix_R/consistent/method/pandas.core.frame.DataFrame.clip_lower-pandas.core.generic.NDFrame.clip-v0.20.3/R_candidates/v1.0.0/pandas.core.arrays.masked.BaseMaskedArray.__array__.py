    def __array__(self, dtype=None) -> np.ndarray:
        """
        the array interface, return my values
        We return an object array here to preserve our scalar values
        """
        return self.to_numpy(dtype=dtype)
