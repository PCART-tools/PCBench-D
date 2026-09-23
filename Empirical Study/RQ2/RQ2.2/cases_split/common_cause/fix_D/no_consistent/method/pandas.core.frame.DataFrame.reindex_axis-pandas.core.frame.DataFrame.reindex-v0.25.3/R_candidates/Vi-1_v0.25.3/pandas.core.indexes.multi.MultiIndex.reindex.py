    def reindex(self, target, method=None, level=None, limit=None, tolerance=None):
        """
        Create index with target's values (move/add/delete values as necessary)

        Returns
        -------
        new_index : pd.MultiIndex
            Resulting index
        indexer : np.ndarray or None
            Indices of output values in original index.

        """
        # GH6552: preserve names when reindexing to non-named target
        # (i.e. neither Index nor Series).
        preserve_names = not hasattr(target, "names")

        if level is not None:
            if method is not None:
                raise TypeError("Fill method not supported if level passed")

            # GH7774: preserve dtype/tz if target is empty and not an Index.
            # target may be an iterator
            target = ibase._ensure_has_len(target)
            if len(target) == 0 and not isinstance(target, Index):
                idx = self.levels[level]
                attrs = idx._get_attributes_dict()
                attrs.pop("freq", None)  # don't preserve freq
                target = type(idx)._simple_new(np.empty(0, dtype=idx.dtype), **attrs)
            else:
                target = ensure_index(target)
            target, indexer, _ = self._join_level(
                target, level, how="right", return_indexers=True, keep_order=False
            )
        else:
            target = ensure_index(target)
            if self.equals(target):
                indexer = None
            else:
                if self.is_unique:
                    indexer = self.get_indexer(
                        target, method=method, limit=limit, tolerance=tolerance
                    )
                else:
                    raise ValueError("cannot handle a non-unique multi-index!")

        if not isinstance(target, MultiIndex):
            if indexer is None:
                target = self
            elif (indexer >= 0).all():
                target = self.take(indexer)
            else:
                # hopefully?
                target = MultiIndex.from_tuples(target)

        if (
            preserve_names
            and target.nlevels == self.nlevels
            and target.names != self.names
        ):
            target = target.copy(deep=False)
            target.names = self.names

        return target, indexer
