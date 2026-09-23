    def _handle_lowerdim_multi_index_axis0(self, tup: Tuple):
        # we have an axis0 multi-index, handle or raise
        axis = self.axis or 0
        try:
            # fast path for series or for tup devoid of slices
            return self._get_label(tup, axis=axis)
        except TypeError:
            # slices are unhashable
            pass
        except KeyError as ek:
            # raise KeyError if number of indexers match
            # else IndexingError will be raised
            if len(tup) <= self.obj.index.nlevels and len(tup) > self.ndim:
                raise ek

        return None
