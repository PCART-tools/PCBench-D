    @property
    def array_values(self) -> ExtensionArray:
        return NumpyExtensionArray(self.values)
