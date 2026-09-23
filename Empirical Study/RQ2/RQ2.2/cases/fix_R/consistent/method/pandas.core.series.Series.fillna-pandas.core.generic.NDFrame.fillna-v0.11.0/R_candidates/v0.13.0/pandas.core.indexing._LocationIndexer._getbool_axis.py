    def _getbool_axis(self, key, axis=0):
            labels = self.obj._get_axis(axis)
            key = _check_bool_indexer(labels, key)
            inds, = key.nonzero()
            try:
                return self.obj.take(inds, axis=axis, convert=False)
            except Exception as detail:
                raise self._exception(detail)
