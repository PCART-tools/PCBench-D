    def fast_2d_xs(self, loc, copy=False):
        """
        get a cross sectional for a given location in the
        items ; handle dups

        return the result and a flag if a copy was actually made
        """
        if len(self.blocks) == 1:
            result = self.blocks[0].values[:, loc]
            if copy:
                result = result.copy()
            return result, copy

        items = self.items

        # non-unique (GH4726)
        if not items.is_unique:
            return self._interleave(items).ravel(), True

        # unique
        dtype = _interleaved_dtype(self.blocks)
        n = len(items)
        result = np.empty(n, dtype=dtype)
        for blk in self.blocks:
            for j, item in enumerate(blk.items):
                i = items.get_loc(item)
                result[i] = blk._try_coerce_result(blk.iget((j, loc)))

        return result, True
