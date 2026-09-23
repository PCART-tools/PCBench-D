    @property
    def dtype(self) -> DtypeObj:
        """
        Return the dtype object of the underlying data.
        """
        return self._mgr.dtype
