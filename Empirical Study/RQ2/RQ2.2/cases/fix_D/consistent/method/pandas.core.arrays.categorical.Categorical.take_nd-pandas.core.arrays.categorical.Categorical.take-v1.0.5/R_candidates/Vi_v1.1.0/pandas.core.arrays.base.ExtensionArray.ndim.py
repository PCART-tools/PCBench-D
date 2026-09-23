    @property
    def ndim(self) -> int:
        """
        Extension Arrays are only allowed to be 1-dimensional.
        """
        return 1
