    def take(self, indexer, axis=0):
        """
        Analogous to ndarray.take
        """
        indexer = com._ensure_platform_int(indexer)
        taken = self.view(np.ndarray).take(indexer)
        return self._constructor(taken, name=self.name)
