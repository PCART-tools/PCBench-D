    def _set_ref_locs(self, labels=None, do_refs=False):
        """
        if we have a non-unique index on this axis, set the indexers
        we need to set an absolute indexer for the blocks
        return the indexer if we are not unique

        labels : the (new) labels for this manager
        ref    : boolean, whether to set the labels (one a 1-1 mapping)

        """

        if labels is None:
            labels = self.items

        # we are unique, and coming from a unique
        is_unique = labels.is_unique
        if is_unique and not do_refs:

            if not self.items.is_unique:

                # reset our ref locs
                self._ref_locs = None
                for b in self.blocks:
                    b._ref_locs = None

            return None

        # we are going to a non-unique index
        # we have ref_locs on the block at this point
        if (not is_unique and do_refs) or do_refs == 'force':

            # create the items map
            im = getattr(self, '_items_map', None)
            if im is None:

                im = dict()
                for block in self.blocks:

                    # if we have a duplicate index but
                    # _ref_locs have not been set
                    try:
                        rl = block.ref_locs
                    except:
                        raise AssertionError(
                            'Cannot create BlockManager._ref_locs because '
                            'block [%s] with duplicate items [%s] does not '
                            'have _ref_locs set' % (block, labels))

                    m = maybe_create_block_in_items_map(im, block)
                    for i, item in enumerate(block.items):
                        m[i] = rl[i]

                self._items_map = im

            # create the _ref_loc map here
            rl = [None] * len(labels)
            for block, items in im.items():
                for i, loc in enumerate(items):
                    rl[loc] = (block, i)
            self._ref_locs = rl
            return rl

        elif do_refs:
            self._reset_ref_locs()

        # return our cached _ref_locs (or will compute again
        # when we recreate the block manager if needed
        return getattr(self, '_ref_locs', None)
