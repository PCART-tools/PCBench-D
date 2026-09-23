    def _getbool_axis(self, key, axis: int):
        # caller is responsible for ensuring non-None axis
        labels = self.obj._get_axis(axis)
        key = check_bool_indexer(labels, key)
        inds, = key.nonzero()
        try:
            return self.obj.take(inds, axis=axis)
        except Exception as detail:
            raise self._exception(detail)
