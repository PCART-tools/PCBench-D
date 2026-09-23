    def set_ref_items(self, ref_items, maybe_rename=True):
        """ we can optimize and our ref_locs are always equal to ref_items """
        if maybe_rename:
            self.items = ref_items
        self.ref_items = ref_items
