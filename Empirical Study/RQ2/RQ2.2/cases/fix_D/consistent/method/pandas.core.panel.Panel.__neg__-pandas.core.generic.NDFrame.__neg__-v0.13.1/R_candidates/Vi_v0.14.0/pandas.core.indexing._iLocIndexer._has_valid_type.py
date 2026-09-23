    def _has_valid_type(self, key, axis):
        if com._is_bool_indexer(key):
            if hasattr(key, 'index') and isinstance(key.index, Index):
                if key.index.inferred_type == 'integer':
                    raise NotImplementedError(
                        "iLocation based boolean indexing on an integer type "
                        "is not available"
                    )
                raise ValueError("iLocation based boolean indexing cannot use "
                                 "an indexable as a mask")
            return True

        if isinstance(key, slice):
            return True
        elif com.is_integer(key):
            return self._is_valid_integer(key, axis)
        elif (_is_list_like(key)):
            return self._is_valid_list_like(key, axis)
        return False
