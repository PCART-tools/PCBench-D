    def _get_setitem_indexer(self, key):
        # GH#32257 Fall through to let numpy do validation
        if is_iterator(key):
            key = list(key)

        if self.axis is not None:
            return self._convert_tuple(key)

        return key
