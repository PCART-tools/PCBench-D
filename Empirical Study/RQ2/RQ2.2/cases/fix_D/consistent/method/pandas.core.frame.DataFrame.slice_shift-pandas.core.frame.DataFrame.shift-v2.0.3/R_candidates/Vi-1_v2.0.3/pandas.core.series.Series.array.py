    @Appender(base.IndexOpsMixin.array.__doc__)  # type: ignore[misc]
    @property
    def array(self) -> ExtensionArray:
        return self._mgr.array_values()
