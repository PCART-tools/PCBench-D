    def get_locs(self, tup):
        """
        Given a tuple of slices/lists/labels/boolean indexer to a level-wise
        spec produce an indexer to extract those locations

        Parameters
        ----------
        key : tuple of (slices/list/labels)

        Returns
        -------
        locs : integer list of locations or boolean indexer suitable
               for passing to iloc
        """

        # must be lexsorted to at least as many levels
        if not self.is_lexsorted_for_tuple(tup):
            raise UnsortedIndexError('MultiIndex Slicing requires the index '
                                     'to be fully lexsorted tuple len ({0}), '
                                     'lexsort depth ({1})'
                                     .format(len(tup), self.lexsort_depth))

        # indexer
        # this is the list of all values that we want to select
        n = len(self)
        indexer = None

        def _convert_to_indexer(r):
            # return an indexer
            if isinstance(r, slice):
                m = np.zeros(n, dtype=bool)
                m[r] = True
                r = m.nonzero()[0]
            elif is_bool_indexer(r):
                if len(r) != n:
                    raise ValueError("cannot index with a boolean indexer "
                                     "that is not the same length as the "
                                     "index")
                r = r.nonzero()[0]
            from .numeric import Int64Index
            return Int64Index(r)

        def _update_indexer(idxr, indexer=indexer):
            if indexer is None:
                indexer = Index(np.arange(n))
            if idxr is None:
                return indexer
            return indexer & idxr

        for i, k in enumerate(tup):

            if is_bool_indexer(k):
                # a boolean indexer, must be the same length!
                k = np.asarray(k)
                indexer = _update_indexer(_convert_to_indexer(k),
                                          indexer=indexer)

            elif is_list_like(k):
                # a collection of labels to include from this level (these
                # are or'd)
                indexers = None
                for x in k:
                    try:
                        idxrs = _convert_to_indexer(
                            self._get_level_indexer(x, level=i,
                                                    indexer=indexer))
                        indexers = (idxrs if indexers is None
                                    else indexers | idxrs)
                    except KeyError:

                        # ignore not founds
                        continue

                if indexers is not None:
                    indexer = _update_indexer(indexers, indexer=indexer)
                else:
                    from .numeric import Int64Index
                    # no matches we are done
                    return Int64Index([])._values

            elif is_null_slice(k):
                # empty slice
                indexer = _update_indexer(None, indexer=indexer)

            elif isinstance(k, slice):

                # a slice, include BOTH of the labels
                indexer = _update_indexer(_convert_to_indexer(
                    self._get_level_indexer(k, level=i, indexer=indexer)),
                    indexer=indexer)
            else:
                # a single label
                indexer = _update_indexer(_convert_to_indexer(
                    self.get_loc_level(k, level=i, drop_level=False)[0]),
                    indexer=indexer)

        # empty indexer
        if indexer is None:
            return Int64Index([])._values
        return indexer._values
