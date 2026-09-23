    @property
    def is_view(self) -> bool:
        """return a boolean if I am possibly a view"""
        values = self.values
        values = cast(np.ndarray, values)
        return values.base is not None
