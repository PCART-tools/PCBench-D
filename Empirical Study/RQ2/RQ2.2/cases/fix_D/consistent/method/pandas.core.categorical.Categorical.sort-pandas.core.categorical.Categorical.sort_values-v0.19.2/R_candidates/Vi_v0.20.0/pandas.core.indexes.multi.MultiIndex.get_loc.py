    def get_loc(self, key, method=None):
        """
        Get integer location, slice or boolean mask for requested label or
        tuple.  If the key is past the lexsort depth, the return may be a
        boolean mask array, otherwise it is always a slice or int.

        Parameters
        ----------
        key : label or tuple
        method : None

        Returns
        -------
        loc : int, slice object or boolean mask
        """
        if method is not None:
            raise NotImplementedError('only the default get_loc method is '
                                      'currently supported for MultiIndex')

        def _maybe_to_slice(loc):
            """convert integer indexer to boolean mask or slice if possible"""
            if not isinstance(loc, np.ndarray) or loc.dtype != 'int64':
                return loc

            loc = lib.maybe_indices_to_slice(loc, len(self))
            if isinstance(loc, slice):
                return loc

            mask = np.empty(len(self), dtype='bool')
            mask.fill(False)
            mask[loc] = True
            return mask

        if not isinstance(key, tuple):
            loc = self._get_level_indexer(key, level=0)
            return _maybe_to_slice(loc)

        keylen = len(key)
        if self.nlevels < keylen:
            raise KeyError('Key length ({0}) exceeds index depth ({1})'
                           ''.format(keylen, self.nlevels))

        if keylen == self.nlevels and self.is_unique:

            def _maybe_str_to_time_stamp(key, lev):
                if lev.is_all_dates and not isinstance(key, Timestamp):
                    try:
                        return Timestamp(key, tz=getattr(lev, 'tz', None))
                    except Exception:
                        pass
                return key

            key = _values_from_object(key)
            key = tuple(map(_maybe_str_to_time_stamp, key, self.levels))
            return self._engine.get_loc(key)

        # -- partial selection or non-unique index
        # break the key into 2 parts based on the lexsort_depth of the index;
        # the first part returns a continuous slice of the index; the 2nd part
        # needs linear search within the slice
        i = self.lexsort_depth
        lead_key, follow_key = key[:i], key[i:]
        start, stop = (self.slice_locs(lead_key, lead_key)
                       if lead_key else (0, len(self)))

        if start == stop:
            raise KeyError(key)

        if not follow_key:
            return slice(start, stop)

        warnings.warn('indexing past lexsort depth may impact performance.',
                      PerformanceWarning, stacklevel=10)

        loc = np.arange(start, stop, dtype='int64')

        for i, k in enumerate(follow_key, len(lead_key)):
            mask = self.labels[i][loc] == self.levels[i].get_loc(k)
            if not mask.all():
                loc = loc[mask]
            if not len(loc):
                raise KeyError(key)

        return (_maybe_to_slice(loc) if len(loc) != stop - start else
                slice(start, stop))
