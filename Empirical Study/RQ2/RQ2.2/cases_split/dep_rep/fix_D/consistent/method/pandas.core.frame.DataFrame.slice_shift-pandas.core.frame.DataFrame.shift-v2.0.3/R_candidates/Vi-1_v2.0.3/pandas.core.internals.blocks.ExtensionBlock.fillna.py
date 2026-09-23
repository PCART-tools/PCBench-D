    def fillna(
        self,
        value,
        limit: int | None = None,
        inplace: bool = False,
        downcast=None,
        using_cow: bool = False,
    ) -> list[Block]:
        if is_interval_dtype(self.dtype):
            # Block.fillna handles coercion (test_fillna_interval)
            return super().fillna(
                value=value,
                limit=limit,
                inplace=inplace,
                downcast=downcast,
                using_cow=using_cow,
            )
        if using_cow and self._can_hold_na and not self.values._hasna:
            refs = self.refs
            new_values = self.values
        else:
            refs = None
            new_values = self.values.fillna(value=value, method=None, limit=limit)
        nb = self.make_block_same_class(new_values, refs=refs)
        return nb._maybe_downcast([nb], downcast, using_cow=using_cow)
