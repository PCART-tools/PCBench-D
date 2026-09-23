    @Appender(_index_shared_docs["_convert_slice_indexer"])
    def _convert_slice_indexer(self, key, kind=None):
        assert kind in ["ix", "loc", "getitem", "iloc", None]

        # if we are not a slice, then we are done
        if not isinstance(key, slice):
            return key

        # validate iloc
        if kind == "iloc":
            return slice(
                self._validate_indexer("slice", key.start, kind),
                self._validate_indexer("slice", key.stop, kind),
                self._validate_indexer("slice", key.step, kind),
            )

        # potentially cast the bounds to integers
        start, stop, step = key.start, key.stop, key.step

        # figure out if this is a positional indexer
        def is_int(v):
            return v is None or is_integer(v)

        is_null_slicer = start is None and stop is None
        is_index_slice = is_int(start) and is_int(stop)
        is_positional = is_index_slice and not self.is_integer()

        if kind == "getitem":
            """
            called from the getitem slicers, validate that we are in fact
            integers
            """
            if self.is_integer() or is_index_slice:
                return slice(
                    self._validate_indexer("slice", key.start, kind),
                    self._validate_indexer("slice", key.stop, kind),
                    self._validate_indexer("slice", key.step, kind),
                )

        # convert the slice to an indexer here

        # if we are mixed and have integers
        try:
            if is_positional and self.is_mixed():
                # Validate start & stop
                if start is not None:
                    self.get_loc(start)
                if stop is not None:
                    self.get_loc(stop)
                is_positional = False
        except KeyError:
            if self.inferred_type == "mixed-integer-float":
                raise

        if is_null_slicer:
            indexer = key
        elif is_positional:
            indexer = key
        else:
            try:
                indexer = self.slice_indexer(start, stop, step, kind=kind)
            except Exception:
                if is_index_slice:
                    if self.is_integer():
                        raise
                    else:
                        indexer = key
                else:
                    raise

        return indexer
