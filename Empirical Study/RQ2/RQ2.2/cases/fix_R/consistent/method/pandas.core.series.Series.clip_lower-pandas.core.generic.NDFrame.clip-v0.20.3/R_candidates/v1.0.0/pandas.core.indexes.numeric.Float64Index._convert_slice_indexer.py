    @Appender(_index_shared_docs["_convert_slice_indexer"])
    def _convert_slice_indexer(self, key, kind=None):
        # if we are not a slice, then we are done
        if not isinstance(key, slice):
            return key

        if kind == "iloc":
            return super()._convert_slice_indexer(key, kind=kind)

        # translate to locations
        return self.slice_indexer(key.start, key.stop, key.step, kind=kind)
