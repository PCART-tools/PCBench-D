    def _getbool_axis(self, key, axis=None):
        if axis is None:
            axis = self.axis or 0
        labels = self.obj._get_axis(axis)
        key = check_bool_indexer(labels, key)
        inds, = key.nonzero()
        try:
            return self.obj._take(inds, axis=axis)
        except Exception as detail:
            raise self._exception(detail)
