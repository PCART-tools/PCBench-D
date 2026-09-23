    def _difference(self, other, sort):

        this = self._get_unique_index()

        indexer = this.get_indexer_for(other)
        indexer = indexer.take((indexer != -1).nonzero()[0])

        label_diff = np.setdiff1d(np.arange(this.size), indexer, assume_unique=True)
        the_diff = this._values.take(label_diff)
        the_diff = _maybe_try_sort(the_diff, sort)

        return the_diff
