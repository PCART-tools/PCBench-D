    def take(self, indexer, axis=None):
        """
        Analogous to ndarray.take
        """
        indexer = com._ensure_platform_int(indexer)
        new_labels = [lab.take(indexer) for lab in self.labels]
        return MultiIndex(levels=self.levels, labels=new_labels,
                          names=self.names, verify_integrity=False)
