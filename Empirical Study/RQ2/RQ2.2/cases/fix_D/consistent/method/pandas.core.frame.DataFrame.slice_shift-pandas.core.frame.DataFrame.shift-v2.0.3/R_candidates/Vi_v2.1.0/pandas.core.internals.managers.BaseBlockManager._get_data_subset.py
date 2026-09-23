    def _get_data_subset(self, predicate: Callable) -> Self:
        blocks = [blk for blk in self.blocks if predicate(blk.values)]
        return self._combine(blocks, copy=False)
