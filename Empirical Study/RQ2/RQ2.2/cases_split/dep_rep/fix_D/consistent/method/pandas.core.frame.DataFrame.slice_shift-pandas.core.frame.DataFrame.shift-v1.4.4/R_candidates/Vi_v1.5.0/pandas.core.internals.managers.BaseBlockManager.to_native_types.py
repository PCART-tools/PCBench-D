    def to_native_types(self: T, **kwargs) -> T:
        """
        Convert values to native types (strings / python objects) that are used
        in formatting (repr / csv).
        """
        return self.apply("to_native_types", **kwargs)
