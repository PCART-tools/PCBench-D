    def _get_slice_axis(self, slice_obj, axis=None):
        obj = self.obj

        if axis is None:
            axis = self.axis or 0

        if not need_slice(slice_obj):
            return obj.copy(deep=False)
        indexer = self._convert_slice_indexer(slice_obj, axis)

        if isinstance(indexer, slice):
            return self._slice(indexer, axis=axis, kind='iloc')
        else:
            return self.obj._take(indexer, axis=axis, convert=False)
