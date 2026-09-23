    def _delete_from_block(self, i, item):
        """
        Delete and maybe remove the whole block

        Remap the split blocks to there old ranges,
        so after this function, _ref_locs and _items_map (if used)
        are correct for the items, None fills holes in _ref_locs
        """
        block = self.blocks.pop(i)
        ref_locs = self._set_ref_locs()
        prev_items_map = self._items_map.pop(
            block) if ref_locs is not None else None

        # if we can't consolidate, then we are removing this block in its
        # entirey
        if block._can_consolidate:

            # compute the split mask
            loc = block.items.get_loc(item)
            if type(loc) == slice or com.is_integer(loc):
                mask = np.array([True] * len(block))
                mask[loc] = False
            else:  # already a mask, inverted
                mask = -loc

            # split the block
            counter = 0
            for s, e in com.split_ranges(mask):

                sblock = make_block(block.values[s:e],
                                    block.items[s:e].copy(),
                                    block.ref_items,
                                    klass=block.__class__,
                                    fastpath=True)

                self.blocks.append(sblock)

                # update the _ref_locs/_items_map
                if ref_locs is not None:

                    # fill the item_map out for this sub-block
                    m = maybe_create_block_in_items_map(
                        self._items_map, sblock)
                    for j, itm in enumerate(sblock.items):

                        # is this item masked (e.g. was deleted)?
                        while (True):

                            if counter > len(mask) or mask[counter]:
                                break
                            else:
                                counter += 1

                        # find my mapping location
                        m[j] = prev_items_map[counter]
                        counter += 1

                    # set the ref_locs in this block
                    sblock.set_ref_locs(m)

        # reset the ref_locs to the new structure
        if ref_locs is not None:

            # items_map is now good, with the original locations
            self._set_ref_locs(do_refs=True)

            # reset the ref_locs based on the now good block._ref_locs
            self._reset_ref_locs()
