    def fillna(self: T, value, limit, inplace: bool, downcast) -> T:
        if limit is not None:
            # Do this validation even if we go through one of the no-op paths
            limit = libalgos.validate_limit(None, limit=limit)

        return self.apply(
            "fillna",
            value=value,
            limit=limit,
            inplace=inplace,
            downcast=downcast,
            using_cow=using_copy_on_write(),
        )
