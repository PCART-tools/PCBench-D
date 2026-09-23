    def take(self, indexer, axis=0):
        """
        return a new Index of the values selected by the indexer

        See also
        --------
        numpy.ndarray.take
        """

        indexer = com._ensure_platform_int(indexer)
        taken = np.array(self).take(indexer)

        # by definition cannot propogate freq
        return self._shallow_copy(taken, freq=None)
