    def _convert_tuple(self, key, is_setter=False):
        keyidx = []
        for i, k in enumerate(key):
            idx = self._convert_to_indexer(k, axis=i, is_setter=is_setter)
            keyidx.append(idx)
        return tuple(keyidx)
