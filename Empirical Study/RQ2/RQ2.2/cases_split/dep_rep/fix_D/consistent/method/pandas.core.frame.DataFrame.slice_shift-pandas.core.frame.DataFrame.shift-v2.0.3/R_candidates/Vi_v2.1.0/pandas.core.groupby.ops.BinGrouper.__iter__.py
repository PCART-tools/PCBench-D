    def __iter__(self) -> Iterator[Hashable]:
        return iter(self.groupings[0].grouping_vector)
