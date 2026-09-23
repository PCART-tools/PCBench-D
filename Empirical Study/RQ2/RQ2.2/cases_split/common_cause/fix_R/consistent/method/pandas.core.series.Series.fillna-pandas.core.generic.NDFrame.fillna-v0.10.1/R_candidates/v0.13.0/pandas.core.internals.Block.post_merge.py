    def post_merge(self, items, **kwargs):
        """ we are non-sparse block, try to convert to a sparse block(s) """
        overlap = set(items.keys()) & set(self.items)
        if len(overlap):
            overlap = _ensure_index(overlap)

            new_blocks = []
            for item in overlap:
                dtypes = set(items[item])

                # this is a safe bet with multiple dtypes
                dtype = list(dtypes)[0] if len(dtypes) == 1 else np.float64

                b = make_block(SparseArray(self.get(item), dtype=dtype),
                               [item], self.ref_items)
                new_blocks.append(b)

            return new_blocks

        return self
