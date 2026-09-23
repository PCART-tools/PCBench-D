    def array_values(self) -> ExtensionArray:
        return TimedeltaArray._simple_new(self.values)
