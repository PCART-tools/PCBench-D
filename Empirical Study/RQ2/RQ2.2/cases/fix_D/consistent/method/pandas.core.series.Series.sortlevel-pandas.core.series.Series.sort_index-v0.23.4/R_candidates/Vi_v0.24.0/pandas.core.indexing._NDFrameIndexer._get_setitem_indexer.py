    def _get_setitem_indexer(self, key):
        if self.axis is not None:
            return self._convert_tuple(key, is_setter=True)

        axis = self.obj._get_axis(0)

        if isinstance(axis, MultiIndex) and self.name != 'iloc':
            try:
                return axis.get_loc(key)
            except Exception:
                pass

        if isinstance(key, tuple):
            try:
                return self._convert_tuple(key, is_setter=True)
            except IndexingError:
                pass

        if isinstance(key, range):
            return self._convert_range(key, is_setter=True)

        try:
            return self._convert_to_indexer(key, is_setter=True)
        except TypeError as e:

            # invalid indexer type vs 'other' indexing errors
            if 'cannot do' in str(e):
                raise
            raise IndexingError(key)
