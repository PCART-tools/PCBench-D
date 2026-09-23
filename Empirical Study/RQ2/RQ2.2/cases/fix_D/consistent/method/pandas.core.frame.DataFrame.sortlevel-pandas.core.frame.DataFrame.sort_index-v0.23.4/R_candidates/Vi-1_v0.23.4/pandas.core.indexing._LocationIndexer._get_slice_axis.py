    def _get_slice_axis(self, slice_obj, axis=None):
        """ this is pretty simple as we just have to deal with labels """
        if axis is None:
            axis = self.axis or 0

        obj = self.obj
        if not need_slice(slice_obj):
            return obj.copy(deep=False)

        labels = obj._get_axis(axis)
        indexer = labels.slice_indexer(slice_obj.start, slice_obj.stop,
                                       slice_obj.step, kind=self.name)

        if isinstance(indexer, slice):
            return self._slice(indexer, axis=axis, kind='iloc')
        else:
            return self.obj._take(indexer, axis=axis)
