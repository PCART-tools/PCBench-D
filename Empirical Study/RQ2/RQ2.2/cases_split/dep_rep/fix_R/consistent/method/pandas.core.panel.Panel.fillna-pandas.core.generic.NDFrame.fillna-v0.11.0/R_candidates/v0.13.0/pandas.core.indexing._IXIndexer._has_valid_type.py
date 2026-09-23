    def _has_valid_type(self, key, axis):
        ax = self.obj._get_axis(axis)

        if isinstance(key, slice):
            return True

        elif com._is_bool_indexer(key):
            return True

        elif _is_list_like(key):
            return True

        else:

            self._convert_scalar_indexer(key, axis)

        return True
