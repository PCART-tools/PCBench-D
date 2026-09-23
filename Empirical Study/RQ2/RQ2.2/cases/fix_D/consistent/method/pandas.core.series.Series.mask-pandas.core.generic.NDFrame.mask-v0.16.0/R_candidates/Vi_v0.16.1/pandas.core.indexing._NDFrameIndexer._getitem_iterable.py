    def _getitem_iterable(self, key, axis=0):
        if self._should_validate_iterable(axis):
            self._has_valid_type(key, axis)

        labels = self.obj._get_axis(axis)

        if is_bool_indexer(key):
            key = check_bool_indexer(labels, key)
            inds, = key.nonzero()
            return self.obj.take(inds, axis=axis, convert=False)
        else:
            if isinstance(key, Index):
                # want Index objects to pass through untouched
                keyarr = key
            else:
                # asarray can be unsafe, NumPy strings are weird
                keyarr = _asarray_tuplesafe(key)

            # have the index handle the indexer and possibly return
            # an indexer or raising
            indexer = labels._convert_list_indexer(keyarr, kind=self.name)
            if indexer is not None:
                return self.obj.take(indexer, axis=axis)

            # this is not the most robust, but...
            if (isinstance(labels, MultiIndex) and len(keyarr) and
                    not isinstance(keyarr[0], tuple)):
                level = 0
            else:
                level = None

            # existing labels are unique and indexer are unique
            if labels.is_unique and Index(keyarr).is_unique:

                try:
                    result = self.obj.reindex_axis(keyarr, axis=axis, level=level)

                    # this is an error as we are trying to find
                    # keys in a multi-index that don't exist
                    if isinstance(labels, MultiIndex) and level is not None:
                        if hasattr(result,'ndim') and not np.prod(result.shape) and len(keyarr):
                            raise KeyError("cannot index a multi-index axis with these keys")

                    return result

                except AttributeError:

                    # Series
                    if axis != 0:
                        raise AssertionError('axis must be 0')
                    return self.obj.reindex(keyarr, level=level)

            # existing labels are non-unique
            else:

                # reindex with the specified axis
                if axis + 1 > self.obj.ndim:
                    raise AssertionError("invalid indexing error with "
                                         "non-unique index")

                new_target, indexer, new_indexer = labels._reindex_non_unique(keyarr)

                if new_indexer is not None:
                    result = self.obj.take(indexer[indexer!=-1], axis=axis,
                                           convert=False)

                    result = result._reindex_with_indexers({
                        axis: [new_target, new_indexer]
                        }, copy=True, allow_dups=True)

                else:
                    result = self.obj.take(indexer, axis=axis,
                                           convert=False)

                return result
