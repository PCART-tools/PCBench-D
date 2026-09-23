    @property
    def codes(self) -> np.ndarray:
        if self._codes is None:
            self._make_codes()
        return self._codes
