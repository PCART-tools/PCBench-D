    def __str__(self) -> str:
        if self._info is not None:
            # Load all keys into self._data
            for tag in self._info:
                self[tag]

        return str(self._data)
