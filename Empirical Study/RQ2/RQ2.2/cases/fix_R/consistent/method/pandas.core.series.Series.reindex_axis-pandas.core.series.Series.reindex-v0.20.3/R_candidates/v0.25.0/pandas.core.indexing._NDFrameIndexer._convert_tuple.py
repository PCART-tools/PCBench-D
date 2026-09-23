    def _convert_tuple(self, key, is_setter: bool = False):
        keyidx = []
        if self.axis is not None:
            axis = self.obj._get_axis_number(self.axis)
            for i in range(self.ndim):
                if i == axis:
                    keyidx.append(
                        self._convert_to_indexer(key, axis=axis, is_setter=is_setter)
                    )
                else:
                    keyidx.append(slice(None))
        else:
            for i, k in enumerate(key):
                if i >= self.obj.ndim:
                    raise IndexingError("Too many indexers")
                idx = self._convert_to_indexer(k, axis=i, is_setter=is_setter)
                keyidx.append(idx)
        return tuple(keyidx)
