    def _add_new_block(self, item, value, loc=None):
        # Do we care about dtype at the moment?

        # hm, elaborate hack?
        if loc is None:
            loc = self.items.get_loc(item)
        new_block = make_block(value, self.items[loc:loc + 1].copy(),
                               self.items, fastpath=True)
        self.blocks.append(new_block)

        # set ref_locs based on the this new block
        # and add to the ref/items maps
        if not self.items.is_unique:

            # insert into the ref_locs at the appropriate location
            # _ref_locs is already long enough,
            # but may need to shift elements
            new_block.set_ref_locs([0])

            # need to shift elements to the right
            if self._ref_locs[loc] is not None:
                for i in reversed(lrange(loc + 1, len(self._ref_locs))):
                    self._ref_locs[i] = self._ref_locs[i - 1]

            self._ref_locs[loc] = (new_block, 0)

            # and reset
            self._reset_ref_locs()
            self._set_ref_locs(do_refs=True)
