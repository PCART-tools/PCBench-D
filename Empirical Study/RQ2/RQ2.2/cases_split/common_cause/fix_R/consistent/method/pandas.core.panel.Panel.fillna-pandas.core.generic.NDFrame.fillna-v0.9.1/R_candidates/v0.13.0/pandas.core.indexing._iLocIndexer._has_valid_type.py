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

        return (isinstance(key, slice) or
                com.is_integer(key) or
                _is_list_like(key))
