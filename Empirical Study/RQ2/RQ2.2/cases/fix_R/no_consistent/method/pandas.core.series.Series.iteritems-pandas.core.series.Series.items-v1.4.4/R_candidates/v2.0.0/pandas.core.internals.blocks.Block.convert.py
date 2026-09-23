    def convert(
        self,
        *,
        copy: bool = True,
        using_cow: bool = False,
    ) -> list[Block]:
        """
        attempt to coerce any object types to better types return a copy
        of the block (if copy = True) by definition we are not an ObjectBlock
        here!
        """
        if not copy and using_cow:
            return [self.copy(deep=False)]
        return [self.copy()] if copy else [self]
