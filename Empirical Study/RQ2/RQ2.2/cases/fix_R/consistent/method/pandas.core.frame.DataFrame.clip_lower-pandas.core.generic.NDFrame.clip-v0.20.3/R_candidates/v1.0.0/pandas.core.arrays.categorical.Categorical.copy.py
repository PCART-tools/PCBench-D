    def copy(self) -> "Categorical":
        """
        Copy constructor.
        """
        return self._constructor(
            values=self._codes.copy(), dtype=self.dtype, fastpath=True
        )
