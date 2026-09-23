    def __array__(self, dtype=None) -> np.ndarray:
        """the array interface, return my values"""
        return self.values
