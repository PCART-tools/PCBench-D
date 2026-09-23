    @final
    def convert(
        self,
        *,
        copy: bool = True,
        using_cow: bool = False,
    ) -> list[Block]:
        """
        Attempt to coerce any object types to better types. Return a copy
        of the block (if copy = True).
        """
        if not self.is_object:
            if not copy and using_cow:
                return [self.copy(deep=False)]
            return [self.copy()] if copy else [self]

        if self.ndim != 1 and self.shape[0] != 1:
            blocks = self.split_and_operate(
                Block.convert, copy=copy, using_cow=using_cow
            )
            if all(blk.dtype.kind == "O" for blk in blocks):
                # Avoid fragmenting the block if convert is a no-op
                if using_cow:
                    return [self.copy(deep=False)]
                return [self.copy()] if copy else [self]
            return blocks

        values = self.values
        if values.ndim == 2:
            # the check above ensures we only get here with values.shape[0] == 1,
            # avoid doing .ravel as that might make a copy
            values = values[0]

        res_values = lib.maybe_convert_objects(
            values,  # type: ignore[arg-type]
            convert_non_numeric=True,
        )
        refs = None
        if copy and res_values is values:
            res_values = values.copy()
        elif res_values is values:
            refs = self.refs

        res_values = ensure_block_shape(res_values, self.ndim)
        res_values = maybe_coerce_values(res_values)
        return [self.make_block(res_values, refs=refs)]
