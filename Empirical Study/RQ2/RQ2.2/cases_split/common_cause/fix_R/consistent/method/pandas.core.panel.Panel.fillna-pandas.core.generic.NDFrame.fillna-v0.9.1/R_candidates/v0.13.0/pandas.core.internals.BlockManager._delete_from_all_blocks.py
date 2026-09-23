    def _delete_from_all_blocks(self, loc, item):
        """ delete from the items loc the item
            the item could be in multiple blocks which could
            change each iteration (as we split blocks) """

        # possibily convert to an indexer
        loc = _possibly_convert_to_indexer(loc)

        if isinstance(loc, (list, tuple, np.ndarray)):
            for l in loc:
                for i, b in enumerate(self.blocks):
                    if item in b.items:
                        self._delete_from_block(i, item)

        else:
            i, _ = self._find_block(item)
            self._delete_from_block(i, item)
