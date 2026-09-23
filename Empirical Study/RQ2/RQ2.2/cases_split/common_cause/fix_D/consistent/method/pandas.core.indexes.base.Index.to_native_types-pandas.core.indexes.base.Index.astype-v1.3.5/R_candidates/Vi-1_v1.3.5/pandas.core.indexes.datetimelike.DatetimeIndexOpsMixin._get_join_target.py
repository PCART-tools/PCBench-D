    def _get_join_target(self) -> np.ndarray:
        return self._data._ndarray.view("i8")
