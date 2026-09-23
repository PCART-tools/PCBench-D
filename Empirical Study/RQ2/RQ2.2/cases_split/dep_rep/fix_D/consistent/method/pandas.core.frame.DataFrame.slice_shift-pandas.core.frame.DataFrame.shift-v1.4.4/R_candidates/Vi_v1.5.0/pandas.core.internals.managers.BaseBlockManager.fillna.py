    def fillna(self: T, value, limit, inplace: bool, downcast) -> T:

        if limit is not None:
            # Do this validation even if we go through one of the no-op paths
            limit = libalgos.validate_limit(None, limit=limit)
        if inplace:
            # TODO(CoW) can be optimized to only copy those blocks that have refs
            if _using_copy_on_write() and any(
                not self._has_no_reference_block(i) for i in range(len(self.blocks))
            ):
                self = self.copy()

        return self.apply(
            "fillna", value=value, limit=limit, inplace=inplace, downcast=downcast
        )
