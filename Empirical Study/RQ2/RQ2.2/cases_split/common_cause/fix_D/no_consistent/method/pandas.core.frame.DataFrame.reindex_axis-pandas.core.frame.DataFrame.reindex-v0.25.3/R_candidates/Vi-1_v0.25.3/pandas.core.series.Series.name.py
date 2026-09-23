    @name.setter
    def name(self, value):
        if value is not None and not is_hashable(value):
            raise TypeError("Series.name must be a hashable type")
        object.__setattr__(self, "_name", value)
