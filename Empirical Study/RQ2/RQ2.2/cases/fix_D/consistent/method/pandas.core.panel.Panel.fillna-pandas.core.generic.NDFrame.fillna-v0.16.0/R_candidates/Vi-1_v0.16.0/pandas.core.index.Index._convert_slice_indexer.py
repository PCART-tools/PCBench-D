    def _convert_slice_indexer(self, key, kind=None):
        """
        convert a slice indexer. disallow floats in the start/stop/step

        Parameters
        ----------
        key : label of the slice bound
        kind : optional, type of the indexing operation (loc/ix/iloc/None)
        """

        # if we are not a slice, then we are done
        if not isinstance(key, slice):
            return key

        # validate iloc
        if kind == 'iloc':

            # need to coerce to_int if needed
            def f(c):
                v = getattr(key,c)
                if v is None or is_integer(v):
                    return v

                # warn if it's a convertible float
                if v == int(v):
                    warnings.warn("slice indexers when using iloc should be integers "
                                  "and not floating point",FutureWarning)
                    return int(v)

                self._invalid_indexer('slice {0} value'.format(c), v)

            return slice(*[ f(c) for c in ['start','stop','step']])

        # validate slicers
        def validate(v):
            if v is None or is_integer(v):
                return True

            # dissallow floats (except for .ix)
            elif is_float(v):
                if kind == 'ix':
                    return True

                return False

            return True
        for c in ['start','stop','step']:
            v = getattr(key,c)
            if not validate(v):
                self._invalid_indexer('slice {0} value'.format(c), v)

        # figure out if this is a positional indexer
        start, stop, step = key.start, key.stop, key.step

        def is_int(v):
            return v is None or is_integer(v)

        is_null_slicer = start is None and stop is None
        is_index_slice = is_int(start) and is_int(stop)
        is_positional = is_index_slice and not self.is_integer()

        if kind == 'getitem':
            return self._convert_slice_indexer_getitem(
                key, is_index_slice=is_index_slice)

        # convert the slice to an indexer here

        # if we are mixed and have integers
        try:
            if is_positional and self.is_mixed():
                if start is not None:
                    i = self.get_loc(start)
                if stop is not None:
                    j = self.get_loc(stop)
                is_positional = False
        except KeyError:
            if self.inferred_type == 'mixed-integer-float':
                raise

        if is_null_slicer:
            indexer = key
        elif is_positional:
            indexer = key
        else:
            try:
                indexer = self.slice_indexer(start, stop, step)
            except Exception:
                if is_index_slice:
                    if self.is_integer():
                        raise
                    else:
                        indexer = key
                else:
                    raise

        return indexer
