    @cache_readonly
    def needs_filling(self):
        for indexer in self.indexers.values():
            # FIXME: cache results of indexer == -1 checks.
            if (indexer == -1).any():
                return True

        return False
