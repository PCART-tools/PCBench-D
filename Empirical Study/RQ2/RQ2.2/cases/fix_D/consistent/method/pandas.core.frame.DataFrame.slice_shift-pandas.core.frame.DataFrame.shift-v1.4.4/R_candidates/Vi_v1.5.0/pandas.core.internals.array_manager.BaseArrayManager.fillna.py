    def fillna(self: T, value, limit, inplace: bool, downcast) -> T:

        if limit is not None:
            # Do this validation even if we go through one of the no-op paths
            limit = libalgos.validate_limit(None, limit=limit)

        return self.apply_with_block(
            "fillna", value=value, limit=limit, inplace=inplace, downcast=downcast
        )
