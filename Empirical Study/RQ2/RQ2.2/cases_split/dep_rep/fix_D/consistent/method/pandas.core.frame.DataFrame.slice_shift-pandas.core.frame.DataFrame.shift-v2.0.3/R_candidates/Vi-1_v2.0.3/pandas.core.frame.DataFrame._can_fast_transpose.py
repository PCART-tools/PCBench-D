    @property
    def _can_fast_transpose(self) -> bool:
        """
        Can we transpose this DataFrame without creating any new array objects.
        """
        if isinstance(self._mgr, ArrayManager):
            return False
        blocks = self._mgr.blocks
        if len(blocks) != 1:
            return False

        dtype = blocks[0].dtype
        # TODO(EA2D) special case would be unnecessary with 2D EAs
        return not is_1d_only_ea_dtype(dtype)
