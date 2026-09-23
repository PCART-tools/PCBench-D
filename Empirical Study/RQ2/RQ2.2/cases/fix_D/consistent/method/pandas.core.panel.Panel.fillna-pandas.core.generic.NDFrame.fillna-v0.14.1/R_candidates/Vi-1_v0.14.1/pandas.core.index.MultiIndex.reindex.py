    def reindex(self, target, method=None, level=None, limit=None,
                copy_if_needed=False):
        """
        Performs any necessary conversion on the input index and calls
        get_indexer. This method is here so MultiIndex and an Index of
        like-labeled tuples can play nice together

        Returns
        -------
        (new_index, indexer, mask) : (MultiIndex, ndarray, ndarray)
        """

        if level is not None:
            if method is not None:
                raise TypeError('Fill method not supported if level passed')
            target = _ensure_index(target)
            target, indexer, _ = self._join_level(target, level, how='right',
                                                  return_indexers=True)
        else:
            if self.equals(target):
                indexer = None
            else:
                if self.is_unique:
                    indexer = self.get_indexer(target, method=method,
                                               limit=limit)
                else:
                    raise Exception(
                        "cannot handle a non-unique multi-index!")

        if not isinstance(target, MultiIndex):
            if indexer is None:
                target = self
            elif (indexer >= 0).all():
                target = self.take(indexer)
            else:
                # hopefully?
                target = MultiIndex.from_tuples(target)

        return target, indexer
