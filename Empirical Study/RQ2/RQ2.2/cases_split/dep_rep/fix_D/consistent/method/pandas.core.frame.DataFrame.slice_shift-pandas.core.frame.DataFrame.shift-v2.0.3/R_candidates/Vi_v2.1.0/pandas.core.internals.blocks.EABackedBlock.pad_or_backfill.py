    @final
    def pad_or_backfill(
        self,
        *,
        method: FillnaOptions,
        axis: AxisInt = 0,
        inplace: bool = False,
        limit: int | None = None,
        limit_area: Literal["inside", "outside"] | None = None,
        downcast: Literal["infer"] | None = None,
        using_cow: bool = False,
    ) -> list[Block]:
        values = self.values
        copy, refs = self._get_refs_and_copy(using_cow, inplace)

        if values.ndim == 2 and axis == 1:
            # NDArrayBackedExtensionArray.fillna assumes axis=0
            new_values = values.T._pad_or_backfill(method=method, limit=limit).T
        else:
            new_values = values._pad_or_backfill(method=method, limit=limit)
        return [self.make_block_same_class(new_values)]
