    def delete(self, item):

        is_unique = self.items.is_unique
        loc = self.items.get_loc(item)

        # dupe keys may return mask
        loc = _possibly_convert_to_indexer(loc)
        self._delete_from_all_blocks(loc, item)

        # _ref_locs, and _items_map are good here
        new_items = self.items.delete(loc)
        self.set_items_norename(new_items)

        self._known_consolidated = False

        if not is_unique:
            self._consolidate_inplace()
