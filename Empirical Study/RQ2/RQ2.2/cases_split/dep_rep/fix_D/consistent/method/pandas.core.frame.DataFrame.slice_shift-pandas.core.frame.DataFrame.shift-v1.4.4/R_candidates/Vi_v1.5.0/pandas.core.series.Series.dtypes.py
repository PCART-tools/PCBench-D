    @property
    def dtypes(self) -> DtypeObj:
        """
        Return the dtype object of the underlying data.
        """
        # DataFrame compatibility
        return self.dtype
