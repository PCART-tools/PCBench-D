    @doc(Index._convert_slice_indexer)
    def _convert_slice_indexer(self, key: slice, kind: str):
        # TODO(2.0): once #45324 deprecation is enforced we should be able
        #  to simplify this.
        if is_float_dtype(self.dtype):
            assert kind in ["loc", "getitem"]

            # TODO: can we write this as a condition based on
            #  e.g. _should_fallback_to_positional?
            # We always treat __getitem__ slicing as label-based
            # translate to locations
            return self.slice_indexer(key.start, key.stop, key.step)

        return super()._convert_slice_indexer(key, kind=kind)
