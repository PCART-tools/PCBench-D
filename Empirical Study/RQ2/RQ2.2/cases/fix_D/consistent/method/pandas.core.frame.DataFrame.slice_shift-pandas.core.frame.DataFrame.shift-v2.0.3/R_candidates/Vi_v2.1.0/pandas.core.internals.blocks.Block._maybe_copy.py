    @final
    def _maybe_copy(self, using_cow: bool, inplace: bool) -> Self:
        if using_cow and inplace:
            deep = self.refs.has_reference()
            blk = self.copy(deep=deep)
        else:
            blk = self if inplace else self.copy()
        return blk
