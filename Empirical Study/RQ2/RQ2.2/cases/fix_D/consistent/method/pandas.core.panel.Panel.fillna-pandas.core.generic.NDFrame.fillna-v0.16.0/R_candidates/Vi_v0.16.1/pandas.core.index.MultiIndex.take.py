    def take(self, indexer, axis=None):
        indexer = com._ensure_platform_int(indexer)
        new_labels = [lab.take(indexer) for lab in self.labels]
        return MultiIndex(levels=self.levels, labels=new_labels,
                          names=self.names, verify_integrity=False)
