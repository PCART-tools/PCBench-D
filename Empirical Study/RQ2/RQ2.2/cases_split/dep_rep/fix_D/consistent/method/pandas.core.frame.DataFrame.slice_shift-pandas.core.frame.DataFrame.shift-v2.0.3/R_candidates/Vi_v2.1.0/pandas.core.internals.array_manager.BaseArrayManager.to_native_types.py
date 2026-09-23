    def to_native_types(self, **kwargs) -> Self:
        return self.apply(to_native_types, **kwargs)
