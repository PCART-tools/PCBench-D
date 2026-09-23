    def get_indexer_for(self, target, **kwargs):
        """ guaranteed return of an indexer even when non-unique """
        if self.is_unique:
            return self.get_indexer(target, **kwargs)
        return self.get_indexer_non_unique(target, **kwargs)[0]
