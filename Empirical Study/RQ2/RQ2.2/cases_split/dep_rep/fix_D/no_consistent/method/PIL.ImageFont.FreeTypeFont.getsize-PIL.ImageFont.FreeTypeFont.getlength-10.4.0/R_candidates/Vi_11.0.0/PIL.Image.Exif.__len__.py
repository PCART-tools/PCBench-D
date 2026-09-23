    def __len__(self) -> int:
        keys = set(self._data)
        if self._info is not None:
            keys.update(self._info)
        return len(keys)
