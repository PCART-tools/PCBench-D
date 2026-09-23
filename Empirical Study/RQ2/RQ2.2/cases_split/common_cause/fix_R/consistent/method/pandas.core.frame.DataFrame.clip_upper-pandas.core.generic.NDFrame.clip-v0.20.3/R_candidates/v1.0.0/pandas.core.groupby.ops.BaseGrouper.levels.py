    @property
    def levels(self) -> List[Index]:
        return [ping.group_index for ping in self.groupings]
