    def _get_level_indexer(self, key, level=0, indexer=None):
        # return an indexer, boolean array or a slice showing where the key is
        # in the totality of values
        # if the indexer is provided, then use this

        level_index = self.levels[level]
        labels = self.labels[level]

        def convert_indexer(start, stop, step, indexer=indexer, labels=labels):
            # given the inputs and the labels/indexer, compute an indexer set
            # if we have a provided indexer, then this need not consider
            # the entire labels set

            r = np.arange(start, stop, step)
            if indexer is not None and len(indexer) != len(labels):

                # we have an indexer which maps the locations in the labels
                # that we have already selected (and is not an indexer for the
                # entire set) otherwise this is wasteful so we only need to
                # examine locations that are in this set the only magic here is
                # that the result are the mappings to the set that we have
                # selected
                from pandas import Series
                mapper = Series(indexer)
                indexer = labels.take(_ensure_platform_int(indexer))
                result = Series(Index(indexer).isin(r).nonzero()[0])
                m = result.map(mapper)._values

            else:
                m = np.zeros(len(labels), dtype=bool)
                m[np.in1d(labels, r,
                          assume_unique=Index(labels).is_unique)] = True

            return m

        if isinstance(key, slice):
            # handle a slice, returnig a slice if we can
            # otherwise a boolean indexer

            try:
                if key.start is not None:
                    start = level_index.get_loc(key.start)
                else:
                    start = 0
                if key.stop is not None:
                    stop = level_index.get_loc(key.stop)
                else:
                    stop = len(level_index) - 1
                step = key.step
            except KeyError:

                # we have a partial slice (like looking up a partial date
                # string)
                start = stop = level_index.slice_indexer(key.start, key.stop,
                                                         key.step, kind='loc')
                step = start.step

            if isinstance(start, slice) or isinstance(stop, slice):
                # we have a slice for start and/or stop
                # a partial date slicer on a DatetimeIndex generates a slice
                # note that the stop ALREADY includes the stopped point (if
                # it was a string sliced)
                return convert_indexer(start.start, stop.stop, step)

            elif level > 0 or self.lexsort_depth == 0 or step is not None:
                # need to have like semantics here to right
                # searching as when we are using a slice
                # so include the stop+1 (so we include stop)
                return convert_indexer(start, stop + 1, step)
            else:
                # sorted, so can return slice object -> view
                i = labels.searchsorted(start, side='left')
                j = labels.searchsorted(stop, side='right')
                return slice(i, j, step)

        else:

            loc = level_index.get_loc(key)
            if isinstance(loc, slice):
                return loc
            elif level > 0 or self.lexsort_depth == 0:
                return np.array(labels == loc, dtype=bool)

            i = labels.searchsorted(loc, side='left')
            j = labels.searchsorted(loc, side='right')
            return slice(i, j)
