    @property
    def _constructor(self: NDFrameT) -> Callable[..., NDFrameT]:
        """
        Used when a manipulation result has the same dimensions as the
        original.
        """
        raise AbstractMethodError(self)
