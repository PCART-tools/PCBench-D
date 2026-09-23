    def _get_slice_axis(self, slice_obj, axis=0):
        obj = self.obj

        if not _need_slice(slice_obj):
            return obj
        indexer = self._convert_slice_indexer(slice_obj, axis)

        if isinstance(indexer, slice):
            return self._slice(indexer, axis=axis, typ='iloc')
        else:
            return self.obj.take(indexer, axis=axis, convert=False)
