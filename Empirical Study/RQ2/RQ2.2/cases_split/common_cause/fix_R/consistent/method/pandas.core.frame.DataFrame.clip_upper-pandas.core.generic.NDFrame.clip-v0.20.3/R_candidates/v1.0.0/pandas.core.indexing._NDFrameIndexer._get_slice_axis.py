    def _get_slice_axis(self, slice_obj: slice, axis: int):
        # caller is responsible for ensuring non-None axis
        obj = self.obj

        if not need_slice(slice_obj):
            return obj.copy(deep=False)

        indexer = self._convert_slice_indexer(slice_obj, axis)
        return self._slice(indexer, axis=axis, kind="iloc")
