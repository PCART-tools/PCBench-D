    @doc(Index._convert_slice_indexer)
    def _convert_slice_indexer(self, key: slice, kind: str):
        assert kind in ["loc", "getitem"]

        # We always treat __getitem__ slicing as label-based
        # translate to locations
        return self.slice_indexer(key.start, key.stop, key.step, kind=kind)
