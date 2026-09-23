    @property
    def _constructor(self) -> Callable[..., Self]:
        """
        Used when a manipulation result has the same dimensions as the
        original.
        """
        raise AbstractMethodError(self)
