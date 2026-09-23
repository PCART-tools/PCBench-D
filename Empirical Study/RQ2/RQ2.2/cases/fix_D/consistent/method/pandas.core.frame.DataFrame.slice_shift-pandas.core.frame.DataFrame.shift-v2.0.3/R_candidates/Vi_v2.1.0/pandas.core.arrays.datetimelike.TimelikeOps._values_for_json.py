    def _values_for_json(self) -> np.ndarray:
        # Small performance bump vs the base class which calls np.asarray(self)
        if isinstance(self.dtype, np.dtype):
            return self._ndarray
        return super()._values_for_json()
