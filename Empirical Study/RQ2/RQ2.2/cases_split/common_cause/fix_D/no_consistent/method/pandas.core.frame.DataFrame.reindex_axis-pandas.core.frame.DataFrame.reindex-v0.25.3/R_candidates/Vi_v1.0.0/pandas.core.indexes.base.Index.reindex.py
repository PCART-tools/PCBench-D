    def reindex(self, target, method=None, level=None, limit=None, tolerance=None):
        """
        Create index with target's values (move/add/delete values
        as necessary).

        Parameters
        ----------
        target : an iterable

        Returns
        -------
        new_index : pd.Index
            Resulting index.
        indexer : np.ndarray or None
            Indices of output values in original index.
        """
        # GH6552: preserve names when reindexing to non-named target
        # (i.e. neither Index nor Series).
        preserve_names = not hasattr(target, "name")

        # GH7774: preserve dtype/tz if target is empty and not an Index.
        target = _ensure_has_len(target)  # target may be an iterator

        if not isinstance(target, Index) and len(target) == 0:
            attrs = self._get_attributes_dict()
            attrs.pop("freq", None)  # don't preserve freq
            values = self._data[:0]  # appropriately-dtyped empty array
            target = self._simple_new(values, dtype=self.dtype, **attrs)
        else:
            target = ensure_index(target)

        if level is not None:
            if method is not None:
                raise TypeError("Fill method not supported if level passed")
            _, indexer, _ = self._join_level(
                target, level, how="right", return_indexers=True
            )
        else:
            if self.equals(target):
                indexer = None
            else:
                # check is_overlapping for IntervalIndex compat
                if self.is_unique and not getattr(self, "is_overlapping", False):
                    indexer = self.get_indexer(
                        target, method=method, limit=limit, tolerance=tolerance
                    )
                else:
                    if method is not None or limit is not None:
                        raise ValueError(
                            "cannot reindex a non-unique index "
                            "with a method or limit"
                        )
                    indexer, missing = self.get_indexer_non_unique(target)

        if preserve_names and target.nlevels == 1 and target.name != self.name:
            target = target.copy()
            target.name = self.name

        return target, indexer
