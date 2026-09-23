    def _get_setitem_indexer(self, key):
        if self.axis is not None:
            return self._convert_tuple(key)

        ax = self.obj._get_axis(0)

        if isinstance(ax, ABCMultiIndex) and self.name != "iloc":
            try:
                return ax.get_loc(key)
            except (TypeError, KeyError, InvalidIndexError):
                # TypeError e.g. passed a bool
                pass

        if isinstance(key, tuple):
            try:
                return self._convert_tuple(key)
            except IndexingError:
                pass

        if isinstance(key, range):
            return list(key)

        axis = self.axis or 0
        try:
            return self._convert_to_indexer(key, axis=axis)
        except TypeError as e:

            # invalid indexer type vs 'other' indexing errors
            if "cannot do" in str(e):
                raise
            raise IndexingError(key)
