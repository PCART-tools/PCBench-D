    def __setitem__(self, key: str, value) -> None:
        if key not in self._keys:
            raise ValueError(f"Unknown flag {key}. Must be one of {self._keys}")
        setattr(self, key, value)
