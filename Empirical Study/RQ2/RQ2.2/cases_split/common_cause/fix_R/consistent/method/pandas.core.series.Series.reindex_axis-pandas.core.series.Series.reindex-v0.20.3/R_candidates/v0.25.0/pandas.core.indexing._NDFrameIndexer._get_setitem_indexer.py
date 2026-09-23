    def _get_setitem_indexer(self, key):
        if self.axis is not None:
            return self._convert_tuple(key, is_setter=True)

        ax = self.obj._get_axis(0)

        if isinstance(ax, MultiIndex) and self.name != "iloc":
            try:
                return ax.get_loc(key)
            except Exception:
                pass

        if isinstance(key, tuple):
            try:
                return self._convert_tuple(key, is_setter=True)
            except IndexingError:
                pass

        if isinstance(key, range):
            return self._convert_range(key, is_setter=True)

        axis = self.axis or 0
        try:
            return self._convert_to_indexer(key, axis=axis, is_setter=True)
        except TypeError as e:

            # invalid indexer type vs 'other' indexing errors
            if "cannot do" in str(e):
                raise
            raise IndexingError(key)
