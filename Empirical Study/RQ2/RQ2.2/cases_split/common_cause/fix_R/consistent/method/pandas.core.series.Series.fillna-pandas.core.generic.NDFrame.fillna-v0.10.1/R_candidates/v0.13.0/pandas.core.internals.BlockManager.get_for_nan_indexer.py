    def get_for_nan_indexer(self, indexer):

        # allow a single nan location indexer
        if not np.isscalar(indexer):
            if len(indexer) == 1:
                indexer = indexer.item()
            else:
                raise ValueError("cannot label index with a null key")

        # take a nan indexer and return the values
        ref_locs = self._set_ref_locs(do_refs='force')
        b, loc = ref_locs[indexer]
        return b.iget(loc)
