    @final
    @maybe_split
    def _downcast_2d(self, dtype) -> list[Block]:
        """
        downcast specialized to 2D case post-validation.

        Refactored to allow use of maybe_split.
        """
        new_values = maybe_downcast_to_dtype(self.values, dtype=dtype)
        return [self.make_block(new_values)]
