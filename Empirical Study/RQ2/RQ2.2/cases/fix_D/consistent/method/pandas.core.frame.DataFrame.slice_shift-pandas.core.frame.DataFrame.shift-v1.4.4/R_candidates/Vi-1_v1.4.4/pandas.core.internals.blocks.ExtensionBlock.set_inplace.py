    def set_inplace(self, locs, values) -> None:
        # NB: This is a misnomer, is supposed to be inplace but is not,
        #  see GH#33457
        # When an ndarray, we should have locs.tolist() == [0]
        # When a BlockPlacement we should have list(locs) == [0]
        self.values = values
        try:
            # TODO(GH33457) this can be removed
            self._cache.clear()
        except AttributeError:
            # _cache not yet initialized
            pass
