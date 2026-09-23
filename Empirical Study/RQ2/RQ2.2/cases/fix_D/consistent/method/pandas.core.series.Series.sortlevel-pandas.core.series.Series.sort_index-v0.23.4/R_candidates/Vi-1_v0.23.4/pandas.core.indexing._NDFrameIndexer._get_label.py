    def _get_label(self, label, axis=None):
        if axis is None:
            axis = self.axis or 0

        if self.ndim == 1:
            # for perf reasons we want to try _xs first
            # as its basically direct indexing
            # but will fail when the index is not present
            # see GH5667
            try:
                return self.obj._xs(label, axis=axis)
            except:
                return self.obj[label]
        elif isinstance(label, tuple) and isinstance(label[axis], slice):
            raise IndexingError('no slices here, handle elsewhere')

        return self.obj._xs(label, axis=axis)
