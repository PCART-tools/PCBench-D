    def __getstate__(self):
        # should not pickle generally (want to share ref_items), but here for
        # completeness
        return (self.items, self.ref_items, self.values)
