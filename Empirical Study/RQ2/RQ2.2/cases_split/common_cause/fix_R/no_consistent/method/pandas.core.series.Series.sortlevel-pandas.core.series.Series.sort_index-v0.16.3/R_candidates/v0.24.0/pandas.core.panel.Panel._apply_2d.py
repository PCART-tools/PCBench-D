    def _apply_2d(self, func, axis):
        """
        Handle 2-d slices, equiv to iterating over the other axis.
        """
        ndim = self.ndim
        axis = [self._get_axis_number(a) for a in axis]

        # construct slabs, in 2-d this is a DataFrame result
        indexer_axis = list(range(ndim))
        for a in axis:
            indexer_axis.remove(a)
        indexer_axis = indexer_axis[0]

        slicer = [slice(None, None)] * ndim
        ax = self._get_axis(indexer_axis)

        results = []
        for i, e in enumerate(ax):
            slicer[indexer_axis] = i
            sliced = self.iloc[tuple(slicer)]

            obj = func(sliced)
            results.append((e, obj))

        return self._construct_return_type(dict(results))
