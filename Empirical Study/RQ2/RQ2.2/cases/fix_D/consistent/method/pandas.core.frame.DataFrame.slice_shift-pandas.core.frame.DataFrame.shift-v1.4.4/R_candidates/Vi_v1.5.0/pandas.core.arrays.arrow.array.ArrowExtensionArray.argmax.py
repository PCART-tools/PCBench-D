    def argmax(self, skipna: bool = True) -> int:
        return self._argmin_max(skipna, "max")
