    def to_native_types(self: T, **kwargs) -> T:
        return self.apply(to_native_types, **kwargs)
