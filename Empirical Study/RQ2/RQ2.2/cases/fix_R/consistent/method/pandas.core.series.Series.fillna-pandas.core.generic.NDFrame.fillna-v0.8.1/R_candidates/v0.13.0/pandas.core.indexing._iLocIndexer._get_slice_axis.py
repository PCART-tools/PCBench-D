    def _get_slice_axis(self, slice_obj, axis=0):
        obj = self.obj

        if not _need_slice(slice_obj):
            return obj

        if isinstance(slice_obj, slice):
            return self._slice(slice_obj, axis=axis, raise_on_error=True,
                               typ='iloc')
        else:
            return self.obj.take(slice_obj, axis=axis, convert=False)
