    def get(self, item):
        """
        Return values for selected item (ndarray or BlockManager).
        """
        if self.items.is_unique:

            if not isnull(item):
                loc = self.items.get_loc(item)
            else:
                indexer = np.arange(len(self.items))[isnull(self.items)]

                # allow a single nan location indexer
                if not np.isscalar(indexer):
                    if len(indexer) == 1:
                        loc = indexer.item()
                    else:
                        raise ValueError("cannot label index with a null key")

            return self.iget(loc)
        else:

            if isnull(item):
                raise ValueError("cannot label index with a null key")

            indexer = self.items.get_indexer_for([item])
            return self.reindex_indexer(new_axis=self.items[indexer],
                                        indexer=indexer, axis=0, allow_dups=True)
