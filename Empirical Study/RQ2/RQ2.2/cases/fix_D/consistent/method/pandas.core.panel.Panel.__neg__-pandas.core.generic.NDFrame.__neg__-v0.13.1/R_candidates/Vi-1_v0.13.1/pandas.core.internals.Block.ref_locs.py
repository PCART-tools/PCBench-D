    @property
    def ref_locs(self):
        if self._ref_locs is None:
            # we have a single block, maybe have duplicates
            # but indexer is easy
            # also if we are not really reindexing, just numbering
            if self._is_single_block or self.ref_items.equals(self.items):
                indexer = np.arange(len(self.items))
            else:

                indexer = self.ref_items.get_indexer(self.items)
                indexer = com._ensure_platform_int(indexer)
                if (indexer == -1).any():

                    # this means that we have nan's in our block
                    try:
                        indexer[indexer == -1] = np.arange(
                            len(self.items))[isnull(self.items)]
                    except:
                        raise AssertionError('Some block items were not in '
                                             'block ref_items')

            self._ref_locs = indexer
        return self._ref_locs
