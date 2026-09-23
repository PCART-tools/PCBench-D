    @property
    def _ndarray(self) -> np.ndarray:
        # NB: A bunch of Interval tests fail if we use ._data
        return self.asi8
