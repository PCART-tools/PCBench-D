    def get(self, item):
        if self.items.is_unique:

            if isnull(item):
                indexer = np.arange(len(self.items))[isnull(self.items)]
                return self.get_for_nan_indexer(indexer)

            _, block = self._find_block(item)
            return block.get(item)
        else:

            if isnull(item):
                raise ValueError("cannot label index with a null key")

            indexer = self.items.get_loc(item)
            ref_locs = np.array(self._set_ref_locs())

            # duplicate index but only a single result
            if com.is_integer(indexer):

                b, loc = ref_locs[indexer]
                values = [b.iget(loc)]
                index = Index([self.items[indexer]])

            # we have a multiple result, potentially across blocks
            else:

                values = [block.iget(i) for block, i in ref_locs[indexer]]
                index = self.items[indexer]

            # create and return a new block manager
            axes = [index] + self.axes[1:]
            blocks = form_blocks(values, index, axes)
            mgr = BlockManager(blocks, axes)
            mgr._consolidate_inplace()
            return mgr
