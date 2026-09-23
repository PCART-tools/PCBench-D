    def __repr__(self) -> str:
        # don't want to print out all of the items here
        name = type(self).__name__
        if self._is_single_block:

            result = f"{name}: {len(self)} dtype: {self.dtype}"

        else:

            shape = " x ".join(pprint_thing(s) for s in self.shape)
            result = (
                f"{name}: {pprint_thing(self.mgr_locs.indexer)}, "
                f"{shape}, dtype: {self.dtype}"
            )

        return result
