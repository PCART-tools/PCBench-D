    def set_axis(self, axis, value, maybe_rename=True, check_axis=True):
        cur_axis, value = self._set_axis(axis, value, check_axis)

        if axis == 0:

            # set/reset ref_locs based on the current index
            # and map the new index if needed
            self._set_ref_locs(labels=cur_axis)

            # take via ref_locs
            for block in self.blocks:
                block.set_ref_items(self.items, maybe_rename=maybe_rename)

            # set/reset ref_locs based on the new index
            self._set_ref_locs(labels=value, do_refs=True)
