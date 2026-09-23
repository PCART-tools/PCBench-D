    @name.setter
    def name(self, value: Optional[Hashable]) -> None:
        if not is_hashable(value):
            raise TypeError("Series.name must be a hashable type")
        object.__setattr__(self, "_name", value)
