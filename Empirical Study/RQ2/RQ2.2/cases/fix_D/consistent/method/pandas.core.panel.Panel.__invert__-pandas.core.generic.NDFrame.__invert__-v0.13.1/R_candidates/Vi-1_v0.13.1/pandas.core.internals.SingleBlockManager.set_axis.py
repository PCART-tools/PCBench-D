    def set_axis(self, axis, value, maybe_rename=True, check_axis=True):
        cur_axis, value = self._set_axis(axis, value, check_axis)
        self._block.set_ref_items(self.items, maybe_rename=maybe_rename)
