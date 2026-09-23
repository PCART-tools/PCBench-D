    def to_native_types(self, **kwargs) -> Self:
        """
        Convert values to native types (strings / python objects) that are used
        in formatting (repr / csv).
        """
        return self.apply("to_native_types", **kwargs)
