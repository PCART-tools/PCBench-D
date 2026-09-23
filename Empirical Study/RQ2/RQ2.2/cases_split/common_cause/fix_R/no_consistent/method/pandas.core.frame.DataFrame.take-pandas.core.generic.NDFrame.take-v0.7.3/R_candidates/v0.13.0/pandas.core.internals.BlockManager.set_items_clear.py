    def set_items_clear(self, value):
        """ clear the ref_locs on all blocks """
        self.set_axis(0, value, maybe_rename='clear', check_axis=False)
