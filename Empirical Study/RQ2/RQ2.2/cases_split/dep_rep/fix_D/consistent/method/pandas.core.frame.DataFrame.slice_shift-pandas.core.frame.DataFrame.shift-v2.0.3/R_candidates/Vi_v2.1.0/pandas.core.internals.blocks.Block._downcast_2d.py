    @final
    @maybe_split
    def _downcast_2d(self, dtype, using_cow: bool = False) -> list[Block]:
        """
        downcast specialized to 2D case post-validation.

        Refactored to allow use of maybe_split.
        """
        new_values = maybe_downcast_to_dtype(self.values, dtype=dtype)
        new_values = maybe_coerce_values(new_values)
        refs = self.refs if new_values is self.values else None
        return [self.make_block(new_values, refs=refs)]
