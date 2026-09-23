    def _getitem_iterable(self, key, axis=0):
        if self._should_validate_iterable(axis):
            self._has_valid_type(key, axis)

        labels = self.obj._get_axis(axis)

        def _reindex(keys, level=None):

            try:
                result = self.obj.reindex_axis(keys, axis=axis, level=level)
            except AttributeError:
                # Series
                if axis != 0:
                    raise AssertionError('axis must be 0')
                return self.obj.reindex(keys, level=level)

            # this is an error as we are trying to find
            # keys in a multi-index that don't exist
            if isinstance(labels, MultiIndex) and level is not None:
                if hasattr(result,'ndim') and not np.prod(result.shape) and len(keys):
                    raise KeyError("cannot index a multi-index axis with these keys")

            return result

        if com._is_bool_indexer(key):
            key = _check_bool_indexer(labels, key)
            inds, = key.nonzero()
            return self.obj.take(inds, axis=axis, convert=False)
        else:
            if isinstance(key, Index):
                # want Index objects to pass through untouched
                keyarr = key
            else:
                # asarray can be unsafe, NumPy strings are weird
                keyarr = _asarray_tuplesafe(key)

            # handle a mixed integer scenario
            indexer = labels._convert_list_indexer_for_mixed(keyarr, typ=self.name)
            if indexer is not None:
                return self.obj.take(indexer, axis=axis)

            # this is not the most robust, but...
            if (isinstance(labels, MultiIndex) and len(keyarr) and
                    not isinstance(keyarr[0], tuple)):
                level = 0
            else:
                level = None

            keyarr_is_unique = Index(keyarr).is_unique

            # existing labels are unique and indexer is unique
            if labels.is_unique and keyarr_is_unique:
                return _reindex(keyarr, level=level)

            else:
                indexer, missing = labels.get_indexer_non_unique(keyarr)
                check = indexer != -1
                result = self.obj.take(indexer[check], axis=axis,
                                       convert=False)

                # need to merge the result labels and the missing labels
                if len(missing):
                    l = np.arange(len(indexer))

                    missing = com._ensure_platform_int(missing)
                    missing_labels = keyarr.take(missing)
                    missing_indexer = com._ensure_int64(l[~check])
                    cur_labels = result._get_axis(axis).values
                    cur_indexer = com._ensure_int64(l[check])

                    new_labels = np.empty(tuple([len(indexer)]), dtype=object)
                    new_labels[cur_indexer] = cur_labels
                    new_labels[missing_indexer] = missing_labels

                    # reindex with the specified axis
                    ndim = self.obj.ndim
                    if axis + 1 > ndim:
                        raise AssertionError("invalid indexing error with "
                                             "non-unique index")

                    # a unique indexer
                    if keyarr_is_unique:

                        # see GH5553, make sure we use the right indexer
                        new_indexer = np.arange(len(indexer))
                        new_indexer[cur_indexer] = np.arange(
                            len(result._get_axis(axis))
                        )
                        new_indexer[missing_indexer] = -1

                    # we have a non_unique selector, need to use the original
                    # indexer here
                    else:

                        # need to retake to have the same size as the indexer
                        rindexer = indexer.values
                        rindexer[~check] = 0
                        result = self.obj.take(rindexer, axis=axis,
                                               convert=False)

                        # reset the new indexer to account for the new size
                        new_indexer = np.arange(len(result))
                        new_indexer[~check] = -1

                    result = result._reindex_with_indexers({
                        axis: [new_labels, new_indexer]
                    }, copy=True, allow_dups=True)

                return result
