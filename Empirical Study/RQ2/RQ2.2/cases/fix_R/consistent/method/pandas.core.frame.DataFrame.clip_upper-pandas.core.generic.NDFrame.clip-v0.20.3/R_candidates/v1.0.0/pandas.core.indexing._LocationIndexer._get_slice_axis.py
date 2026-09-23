    def _get_slice_axis(self, slice_obj: slice, axis: int):
        """
        This is pretty simple as we just have to deal with labels.
        """
        # caller is responsible for ensuring non-None axis
        obj = self.obj
        if not need_slice(slice_obj):
            return obj.copy(deep=False)

        labels = obj._get_axis(axis)
        indexer = labels.slice_indexer(
            slice_obj.start, slice_obj.stop, slice_obj.step, kind=self.name
        )

        if isinstance(indexer, slice):
            return self._slice(indexer, axis=axis, kind="iloc")
        else:
            # DatetimeIndex overrides Index.slice_indexer and may
            #  return a DatetimeIndex instead of a slice object.
            return self.obj._take_with_is_copy(indexer, axis=axis)
