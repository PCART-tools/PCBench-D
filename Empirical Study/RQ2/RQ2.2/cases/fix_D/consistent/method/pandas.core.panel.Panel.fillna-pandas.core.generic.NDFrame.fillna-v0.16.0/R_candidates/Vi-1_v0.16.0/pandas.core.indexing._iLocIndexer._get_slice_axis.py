    def _get_slice_axis(self, slice_obj, axis=0):
        obj = self.obj

        if not need_slice(slice_obj):
            return obj

        slice_obj = self._convert_slice_indexer(slice_obj, axis)
        if isinstance(slice_obj, slice):
            return self._slice(slice_obj, axis=axis, kind='iloc')
        else:
            return self.obj.take(slice_obj, axis=axis, convert=False)
