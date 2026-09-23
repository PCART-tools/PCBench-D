    def pad_or_backfill(self, inplace: bool, **kwargs) -> Self:
        return self.apply_with_block(
            "pad_or_backfill",
            inplace=inplace,
            **kwargs,
            using_cow=using_copy_on_write(),
        )
