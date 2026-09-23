    def _get_level_indexer(self, key, level=0):
        # return a boolean indexer or a slice showing where the key is
        # in the totality of values

        level_index = self.levels[level]
        labels = self.labels[level]

        if isinstance(key, slice):
            # handle a slice, returnig a slice if we can
            # otherwise a boolean indexer

            start = level_index.get_loc(key.start or  0)
            stop  = level_index.get_loc(key.stop or len(level_index)-1)
            step = key.step

            if isinstance(start,slice) or isinstance(stop,slice):
                # we have a slice for start and/or stop
                # a partial date slicer on a DatetimeIndex generates a slice
                # note that the stop ALREADY includes the stopped point (if
                # it was a string sliced)
                m = np.zeros(len(labels),dtype=bool)
                m[np.in1d(labels,np.arange(start.start,stop.stop,step))] = True
                return m

            elif level > 0 or self.lexsort_depth == 0 or step is not None:
                # need to have like semantics here to right
                # searching as when we are using a slice
                # so include the stop+1 (so we include stop)
                m = np.zeros(len(labels),dtype=bool)
                m[np.in1d(labels,np.arange(start,stop+1,step))] = True
                return m
            else:
                # sorted, so can return slice object -> view
                i = labels.searchsorted(start, side='left')
                j = labels.searchsorted(stop, side='right')
                return slice(i, j, step)

        else:

            loc = level_index.get_loc(key)
            if level > 0 or self.lexsort_depth == 0:
                return np.array(labels == loc,dtype=bool)
            else:
                # sorted, so can return slice object -> view
                i = labels.searchsorted(loc, side='left')
                j = labels.searchsorted(loc, side='right')
                return slice(i, j)
