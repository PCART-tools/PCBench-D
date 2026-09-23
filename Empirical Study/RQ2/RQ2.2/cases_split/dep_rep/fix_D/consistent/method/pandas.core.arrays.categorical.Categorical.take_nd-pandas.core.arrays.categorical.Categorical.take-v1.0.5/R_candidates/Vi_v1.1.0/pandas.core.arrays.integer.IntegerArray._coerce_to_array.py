    def _coerce_to_array(self, value) -> Tuple[np.ndarray, np.ndarray]:
        return coerce_to_array(value, dtype=self.dtype)
