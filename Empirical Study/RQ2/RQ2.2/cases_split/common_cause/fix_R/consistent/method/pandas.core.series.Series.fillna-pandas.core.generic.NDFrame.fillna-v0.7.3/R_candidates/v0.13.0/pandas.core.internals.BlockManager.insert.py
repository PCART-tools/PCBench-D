    def insert(self, loc, item, value, allow_duplicates=False):

        if not allow_duplicates and item in self.items:
            # Should this be a different kind of error??
            raise ValueError('cannot insert %s, already exists' % item)

        try:
            new_items = self.items.insert(loc, item)
            self.set_items_norename(new_items)

            # new block
            self._add_new_block(item, value, loc=loc)

        except:

            # so our insertion operation failed, so back out of the new items
            # GH 3010
            new_items = self.items.delete(loc)
            self.set_items_norename(new_items)

            # re-raise
            raise

        if len(self.blocks) > 100:
            self._consolidate_inplace()

        self._known_consolidated = False

        # clear the internal ref_loc mappings if necessary
        if loc != len(self.items) - 1 and new_items.is_unique:
            self.set_items_clear(new_items)
