    @attrs.setter
    def attrs(self, value: Mapping[Optional[Hashable], Any]) -> None:
        self._attrs = dict(value)
