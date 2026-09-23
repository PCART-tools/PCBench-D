    def _apply_1d(self, func, axis):

        axis_name = self._get_axis_name(axis)
        ndim = self.ndim
        values = self.values

        # iter thru the axes
        slice_axis = self._get_axis(axis)
        slice_indexer = [0] * (ndim - 1)
        indexer = np.zeros(ndim, 'O')
        indlist = list(range(ndim))
        indlist.remove(axis)
        indexer[axis] = slice(None, None)
        indexer.put(indlist, slice_indexer)
        planes = [self._get_axis(axi) for axi in indlist]
        shape = np.array(self.shape).take(indlist)

        # all the iteration points
        points = cartesian_product(planes)

        results = []
        for i in range(np.prod(shape)):

            # construct the object
            pts = tuple(p[i] for p in points)
            indexer.put(indlist, slice_indexer)

            obj = Series(values[tuple(indexer)], index=slice_axis, name=pts)
            result = func(obj)

            results.append(result)

            # increment the indexer
            slice_indexer[-1] += 1
            n = -1
            while (slice_indexer[n] >= shape[n]) and (n > (1 - ndim)):
                slice_indexer[n - 1] += 1
                slice_indexer[n] = 0
                n -= 1

        # empty object
        if not len(results):
            return self._constructor(**self._construct_axes_dict())

        # same ndim as current
        if isinstance(results[0], Series):
            arr = np.vstack([r.values for r in results])
            arr = arr.T.reshape(tuple([len(slice_axis)] + list(shape)))
            tranp = np.array([axis] + indlist).argsort()
            arr = arr.transpose(tuple(list(tranp)))
            return self._constructor(arr, **self._construct_axes_dict())

        # ndim-1 shape
        results = np.array(results).reshape(shape)
        if results.ndim == 2 and axis_name != self._info_axis_name:
            results = results.T
            planes = planes[::-1]
        return self._construct_return_type(results, planes)
