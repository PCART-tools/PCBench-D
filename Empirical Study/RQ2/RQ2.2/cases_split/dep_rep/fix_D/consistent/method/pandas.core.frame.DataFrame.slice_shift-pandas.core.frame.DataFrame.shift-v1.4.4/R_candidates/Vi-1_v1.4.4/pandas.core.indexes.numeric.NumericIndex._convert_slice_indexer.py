    @doc(Index._convert_slice_indexer)
    def _convert_slice_indexer(self, key: slice, kind: str):
        if is_float_dtype(self.dtype):
            assert kind in ["loc", "getitem"]

            # We always treat __getitem__ slicing as label-based
            # translate to locations
            return self.slice_indexer(key.start, key.stop, key.step)

        return super()._convert_slice_indexer(key, kind=kind)
