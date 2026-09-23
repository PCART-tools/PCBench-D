    def set(self, item, value):
        """
        Set new item in-place. Does not consolidate. Adds new Block if not
        contained in the current set of items
        """
        if not isinstance(value, SparseArray):
            if value.ndim == self.ndim - 1:
                value = value.reshape((1,) + value.shape)
            if value.shape[1:] != self.shape[1:]:
                raise AssertionError('Shape of new values must be compatible '
                                     'with manager shape')

        def _set_item(item, arr):
            i, block = self._find_block(item)
            if not block.should_store(value):
                # delete from block, create and append new block
                self._delete_from_block(i, item)
                self._add_new_block(item, arr, loc=None)
            else:
                block.set(item, arr)

        try:

            loc = self.items.get_loc(item)
            if isinstance(loc, int):
                _set_item(self.items[loc], value)
            else:
                subset = self.items[loc]
                if len(value) != len(subset):
                    raise AssertionError(
                        'Number of items to set did not match')

                # we are inserting multiple non-unique items as replacements
                # we are inserting one by one, so the index can go from unique
                # to non-unique during the loop, need to have _ref_locs defined
                # at all times
                if np.isscalar(item) and com.is_list_like(loc):

                    # first delete from all blocks
                    self.delete(item)

                    loc = _possibly_convert_to_indexer(loc)
                    for i, (l, k, arr) in enumerate(zip(loc, subset, value)):

                        # insert the item
                        self.insert(
                            l, k, arr[None, :], allow_duplicates=True)

                        # reset the _ref_locs on indiviual blocks
                        # rebuild ref_locs
                        if self.items.is_unique:
                            self._reset_ref_locs()
                            self._set_ref_locs(do_refs='force')

                    self._rebuild_ref_locs()

                else:
                    for i, (item, arr) in enumerate(zip(subset, value)):
                        _set_item(item, arr[None, :])
        except KeyError:
            # insert at end
            self.insert(len(self.items), item, value)

        self._known_consolidated = False
