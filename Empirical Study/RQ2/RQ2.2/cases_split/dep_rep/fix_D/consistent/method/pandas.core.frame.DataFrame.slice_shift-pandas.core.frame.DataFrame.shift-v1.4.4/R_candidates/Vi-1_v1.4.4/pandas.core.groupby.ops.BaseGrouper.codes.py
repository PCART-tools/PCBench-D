    @final
    @property
    def codes(self) -> list[np.ndarray]:
        return [ping.codes for ping in self.groupings]
