    def _get_setitem_indexer(self, key):
        # GH#32257 Fall through to let numpy do validation
        if is_iterator(key):
            key = list(key)

        if self.axis is not None:
            key = _tupleize_axis_indexer(self.ndim, self.axis, key)

        return key
