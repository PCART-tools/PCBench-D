    def _get_data_subset(self: T, predicate: Callable) -> T:
        blocks = [blk for blk in self.blocks if predicate(blk.values)]
        return self._combine(blocks, copy=False)
