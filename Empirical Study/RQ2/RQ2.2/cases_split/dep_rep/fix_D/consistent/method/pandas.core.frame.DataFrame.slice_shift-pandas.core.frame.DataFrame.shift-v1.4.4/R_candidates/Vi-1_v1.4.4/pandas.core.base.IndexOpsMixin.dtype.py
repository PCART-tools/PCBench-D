    @property
    def dtype(self) -> DtypeObj:
        # must be defined here as a property for mypy
        raise AbstractMethodError(self)
