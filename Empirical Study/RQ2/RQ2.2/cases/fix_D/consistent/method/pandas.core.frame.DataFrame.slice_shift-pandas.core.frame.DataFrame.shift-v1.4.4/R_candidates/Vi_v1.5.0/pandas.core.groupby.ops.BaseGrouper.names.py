    @property
    def names(self) -> list[Hashable]:
        return [ping.name for ping in self.groupings]
