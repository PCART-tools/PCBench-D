    @property
    def _is_monotonic_increasing(self) -> bool:
        return algos.is_monotonic(self.asi8, timelike=True)[0]
