    def _has_valid_type(self, key, axis):
        if isinstance(key, slice):
            return True

        elif is_bool_indexer(key):
            return True

        elif is_list_like_indexer(key):
            return True

        else:

            self._convert_scalar_indexer(key, axis)

        return True
