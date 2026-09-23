    def order(self, return_indexer=False, ascending=True):
        """
        Return sorted copy of Index
        """
        _as = self.argsort()
        if not ascending:
            _as = _as[::-1]

        sorted_index = self.take(_as)

        if return_indexer:
            return sorted_index, _as
        else:
            return sorted_index
