    @final
    def fillna(self, value, limit: int | None, inplace: bool, downcast) -> Self:
        if limit is not None:
            # Do this validation even if we go through one of the no-op paths
            limit = libalgos.validate_limit(None, limit=limit)

        return self.apply_with_block(
            "fillna",
            value=value,
            limit=limit,
            inplace=inplace,
            downcast=downcast,
            using_cow=using_copy_on_write(),
        )
