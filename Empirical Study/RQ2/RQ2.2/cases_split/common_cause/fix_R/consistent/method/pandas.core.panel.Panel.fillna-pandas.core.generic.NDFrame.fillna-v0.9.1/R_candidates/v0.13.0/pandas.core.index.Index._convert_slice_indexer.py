    def _convert_slice_indexer(self, key, typ=None):
        """ convert a slice indexer. disallow floats in the start/stop/step """

        # validate slicers
        def validate(v):
            if v is None or is_integer(v):
                return True

            # dissallow floats
            elif is_float(v):
                return False

            return True

        self._validate_slicer(key, validate)

        # figure out if this is a positional indexer
        start, stop, step = key.start, key.stop, key.step

        def is_int(v):
            return v is None or is_integer(v)

        is_null_slice = start is None and stop is None
        is_index_slice = is_int(start) and is_int(stop)
        is_positional = is_index_slice and not self.is_integer()

        if typ == 'iloc':
            return self._convert_slice_indexer_iloc(key)
        elif typ == 'getitem':
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

        if is_null_slice:
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
