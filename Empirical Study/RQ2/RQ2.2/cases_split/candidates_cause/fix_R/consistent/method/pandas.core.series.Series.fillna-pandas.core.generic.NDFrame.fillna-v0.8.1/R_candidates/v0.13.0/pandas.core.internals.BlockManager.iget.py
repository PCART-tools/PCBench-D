    def iget(self, i):
        item = self.items[i]

        # unique
        if self.items.is_unique:
            if notnull(item):
                return self.get(item)
            return self.get_for_nan_indexer(i)

        ref_locs = self._set_ref_locs()
        b, loc = ref_locs[i]
        return b.iget(loc)
