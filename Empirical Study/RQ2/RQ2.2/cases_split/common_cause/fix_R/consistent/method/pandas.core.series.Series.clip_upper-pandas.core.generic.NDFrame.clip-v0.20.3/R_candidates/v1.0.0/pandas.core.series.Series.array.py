    @Appender(base.IndexOpsMixin.array.__doc__)  # type: ignore
    @property
    def array(self) -> ExtensionArray:
        return self._data._block.array_values()
