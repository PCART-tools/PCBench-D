    @property
    def numpy_dtype(self) -> np.dtype:
        """
        The NumPy dtype this PandasDtype wraps.
        """
        return self._dtype
