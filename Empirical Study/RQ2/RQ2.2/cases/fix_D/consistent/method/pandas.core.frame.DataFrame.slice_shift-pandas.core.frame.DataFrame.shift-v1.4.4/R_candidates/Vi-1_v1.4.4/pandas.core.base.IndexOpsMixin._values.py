    @property
    def _values(self) -> ExtensionArray | np.ndarray:
        # must be defined here as a property for mypy
        raise AbstractMethodError(self)
