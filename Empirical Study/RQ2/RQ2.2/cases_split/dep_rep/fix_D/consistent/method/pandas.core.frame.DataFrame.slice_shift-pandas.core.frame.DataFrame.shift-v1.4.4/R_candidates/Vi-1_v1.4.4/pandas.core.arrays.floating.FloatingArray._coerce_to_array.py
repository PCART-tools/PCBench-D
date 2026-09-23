    def _coerce_to_array(self, value) -> tuple[np.ndarray, np.ndarray]:
        return coerce_to_array(value, dtype=self.dtype)
