    @property
    def levels(self) -> list[Index]:
        return [ping.group_index for ping in self.groupings]
