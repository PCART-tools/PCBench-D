    def take(self, indexer, new_index=None, axis=1, verify=True):
        if axis < 1:
            raise AssertionError('axis must be at least 1, got %d' % axis)

        self._consolidate_inplace()
        if isinstance(indexer, list):
            indexer = np.array(indexer)

        indexer = com._ensure_platform_int(indexer)
        n = len(self.axes[axis])

        if verify:
            indexer = _maybe_convert_indices(indexer, n)
            if ((indexer == -1) | (indexer >= n)).any():
                raise Exception('Indices must be nonzero and less than '
                                'the axis length')

        new_axes = list(self.axes)
        if new_index is None:
            new_index = self.axes[axis].take(indexer)

        new_axes[axis] = new_index
        return self.apply('take',
                          axes=new_axes,
                          indexer=indexer,
                          ref_items=new_axes[0],
                          new_axis=new_axes[axis],
                          axis=axis)
