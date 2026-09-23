    @Appender(_NDFrameIndexer._validate_key.__doc__)
    def _validate_key(self, key, axis: int):
        if isinstance(key, slice):
            return True

        elif com.is_bool_indexer(key):
            return True

        elif is_list_like_indexer(key):
            return True

        else:

            self._convert_scalar_indexer(key, axis)

        return True
