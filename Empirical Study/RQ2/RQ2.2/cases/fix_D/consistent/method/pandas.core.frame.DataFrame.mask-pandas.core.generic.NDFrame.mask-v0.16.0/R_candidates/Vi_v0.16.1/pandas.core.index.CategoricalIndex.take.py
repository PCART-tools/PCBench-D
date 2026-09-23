    def take(self, indexer, axis=0):
        """
        return a new CategoricalIndex of the values selected by the indexer

        See also
        --------
        numpy.ndarray.take
        """

        indexer = com._ensure_platform_int(indexer)
        taken = self.codes.take(indexer)
        return self._create_from_codes(taken)
