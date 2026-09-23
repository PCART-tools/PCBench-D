    @property
    def _constructor(self: FrameOrSeries) -> Type[FrameOrSeries]:
        """Used when a manipulation result has the same dimensions as the
        original.
        """
        raise AbstractMethodError(self)
