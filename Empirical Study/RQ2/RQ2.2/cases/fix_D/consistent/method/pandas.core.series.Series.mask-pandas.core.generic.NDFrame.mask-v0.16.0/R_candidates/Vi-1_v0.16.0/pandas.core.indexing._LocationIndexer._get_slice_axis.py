    def _get_slice_axis(self, slice_obj, axis=0):
        """ this is pretty simple as we just have to deal with labels """
        obj = self.obj
        if not need_slice(slice_obj):
            return obj

        labels = obj._get_axis(axis)
        indexer = labels.slice_indexer(slice_obj.start, slice_obj.stop,
                                       slice_obj.step)

        if isinstance(indexer, slice):
            return self._slice(indexer, axis=axis, kind='iloc')
        else:
            return self.obj.take(indexer, axis=axis, convert=False)
