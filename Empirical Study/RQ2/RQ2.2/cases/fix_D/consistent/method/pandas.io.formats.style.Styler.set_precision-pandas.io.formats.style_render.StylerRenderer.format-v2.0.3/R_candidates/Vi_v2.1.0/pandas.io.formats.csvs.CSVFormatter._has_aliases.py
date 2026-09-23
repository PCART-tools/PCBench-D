    @property
    def _has_aliases(self) -> bool:
        return isinstance(self.header, (tuple, list, np.ndarray, ABCIndex))
