    def argmin(self, skipna: bool = True) -> int:
        return self._argmin_max(skipna, "min")
