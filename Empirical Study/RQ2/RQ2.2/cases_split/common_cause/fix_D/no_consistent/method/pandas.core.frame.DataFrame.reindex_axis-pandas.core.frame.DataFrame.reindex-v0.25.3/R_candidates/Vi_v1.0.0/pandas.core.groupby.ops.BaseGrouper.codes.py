    @property
    def codes(self) -> List[np.ndarray]:
        return [ping.codes for ping in self.groupings]
