    @property
    def values(self) -> np.ndarray:
        # NB: For Datetime64TZ this is lossy
        return self._data._ndarray
