    def reindex(self, target, method=None, level=None, limit=None,
                copy_if_needed=False, takeable=False):
        """
        For Index, simply returns the new index and the results of
        get_indexer. Provided here to enable an interface that is amenable for
        subclasses of Index whose internals are different (like MultiIndex)

        Returns
        -------
        (new_index, indexer, mask) : tuple
        """
        target = _ensure_index(target)
        if level is not None:
            if method is not None:
                raise TypeError('Fill method not supported if level passed')
            _, indexer, _ = self._join_level(target, level, how='right',
                                             return_indexers=True)
        else:

            if self.equals(target):
                indexer = None

                # to avoid aliasing an existing index
                if (copy_if_needed and target.name != self.name and
                        self.name is not None):
                    if target.name is None:
                        target = self.copy()

            else:

                if takeable:
                    if method is not None or limit is not None:
                        raise ValueError("cannot do a takeable reindex with "
                                         "with a method or limit")
                    return self[target], target

                if self.is_unique:
                    indexer = self.get_indexer(target, method=method,
                                               limit=limit)
                else:
                    if method is not None or limit is not None:
                        raise ValueError("cannot reindex a non-unique index "
                                         "with a method or limit")
                    indexer, missing = self.get_indexer_non_unique(target)

        return target, indexer
