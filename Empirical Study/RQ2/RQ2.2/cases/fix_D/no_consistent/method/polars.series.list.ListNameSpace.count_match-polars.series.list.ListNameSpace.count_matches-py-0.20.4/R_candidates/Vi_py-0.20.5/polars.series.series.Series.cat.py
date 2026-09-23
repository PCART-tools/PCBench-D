    @property
    def cat(self) -> CatNameSpace:
        """Create an object namespace of all categorical related methods."""
        return CatNameSpace(self)
