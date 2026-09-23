    def _difference(self, other, sort):

        this = self._get_unique_index()

        indexer = this.get_indexer(other)
        indexer = indexer.take((indexer != -1).nonzero()[0])

        label_diff = np.setdiff1d(np.arange(this.size), indexer, assume_unique=True)
        the_diff = this._values.take(label_diff)
        if sort is None:
            try:
                the_diff = algos.safe_sort(the_diff)
            except TypeError:
                pass

        return the_diff
