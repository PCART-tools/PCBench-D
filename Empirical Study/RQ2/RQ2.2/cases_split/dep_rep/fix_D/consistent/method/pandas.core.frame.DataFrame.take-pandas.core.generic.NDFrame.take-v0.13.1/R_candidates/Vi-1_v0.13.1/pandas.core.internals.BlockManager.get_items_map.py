    def get_items_map(self, use_cached=True):
        """
        return an inverted ref_loc map for an item index
        block -> item (in that block) location -> column location

        use_cached : boolean, use the cached items map, or recreate
        """

        # cache check
        if use_cached:
            im = getattr(self, '_items_map', None)
            if im is not None:
                return im

        im = dict()
        rl = self._set_ref_locs()

        # we have a non-duplicative index
        if rl is None:

            axis = self.axes[0]
            for block in self.blocks:

                m = maybe_create_block_in_items_map(im, block)
                for i, item in enumerate(block.items):
                    m[i] = axis.get_loc(item)

        # use the ref_locs to construct the map
        else:

            for i, (block, idx) in enumerate(rl):

                m = maybe_create_block_in_items_map(im, block)
                m[idx] = i

        self._items_map = im
        return im
