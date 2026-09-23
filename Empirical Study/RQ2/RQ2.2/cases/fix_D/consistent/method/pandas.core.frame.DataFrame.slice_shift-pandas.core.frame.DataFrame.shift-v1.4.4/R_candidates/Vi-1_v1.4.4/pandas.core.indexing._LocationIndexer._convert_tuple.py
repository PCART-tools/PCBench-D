    def _convert_tuple(self, key):
        keyidx = []
        if self.axis is not None:
            axis = self.obj._get_axis_number(self.axis)
            for i in range(self.ndim):
                if i == axis:
                    keyidx.append(self._convert_to_indexer(key, axis=axis))
                else:
                    keyidx.append(slice(None))
        else:
            self._validate_key_length(key)
            for i, k in enumerate(key):
                idx = self._convert_to_indexer(k, axis=i)
                keyidx.append(idx)

        return tuple(keyidx)
