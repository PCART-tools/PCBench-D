    def _getbool_axis(self, key, axis: int):
        # caller is responsible for ensuring non-None axis
        labels = self.obj._get_axis(axis)
        key = check_bool_indexer(labels, key)
        inds = key.nonzero()[0]
        return self.obj._take_with_is_copy(inds, axis=axis)
