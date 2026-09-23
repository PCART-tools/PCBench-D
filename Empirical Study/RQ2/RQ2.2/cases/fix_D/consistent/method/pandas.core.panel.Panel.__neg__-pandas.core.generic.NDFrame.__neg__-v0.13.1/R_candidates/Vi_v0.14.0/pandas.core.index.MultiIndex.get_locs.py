    def get_locs(self, tup):
        """
        Given a tuple of slices/lists/labels/boolean indexer to a level-wise spec
        produce an indexer to extract those locations

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
            raise KeyError('MultiIndex Slicing requires the index to be fully lexsorted'
                           ' tuple len ({0}), lexsort depth ({1})'.format(len(tup), self.lexsort_depth))

        def _convert_indexer(r):
            if isinstance(r, slice):
                m = np.zeros(len(self),dtype=bool)
                m[r] = True
                return m
            return r

        ranges = []
        for i,k in enumerate(tup):

            if com._is_bool_indexer(k):
                # a boolean indexer, must be the same length!
                k = np.asarray(k)
                if len(k) != len(self):
                    raise ValueError("cannot index with a boolean indexer that is"
                                     " not the same length as the index")
                ranges.append(k)
            elif com.is_list_like(k):
                # a collection of labels to include from this level (these are or'd)
                ranges.append(reduce(
                    np.logical_or,[ _convert_indexer(self._get_level_indexer(x, level=i)
                                                     ) for x in k ]))
            elif k == slice(None):
                # include all from this level
                pass
            elif isinstance(k,slice):
                # a slice, include BOTH of the labels
                ranges.append(self._get_level_indexer(k,level=i))
            else:
                # a single label
                ranges.append(self.get_loc_level(k,level=i,drop_level=False)[0])

        # identity
        if len(ranges) == 0:
            return slice(0,len(self))

        elif len(ranges) == 1:
            return ranges[0]

        # construct a boolean indexer if we have a slice or boolean indexer
        return reduce(np.logical_and,[ _convert_indexer(r) for r in ranges ])
