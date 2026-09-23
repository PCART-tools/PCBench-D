    def _get_sample_object(
        self,
        objs: list[Series | DataFrame],
        ndims: set[int],
        keys,
        names,
        levels,
    ) -> tuple[Series | DataFrame, list[Series | DataFrame]]:
        # get the sample
        # want the highest ndim that we have, and must be non-empty
        # unless all objs are empty
        sample: Series | DataFrame | None = None
        if len(ndims) > 1:
            max_ndim = max(ndims)
            for obj in objs:
                if obj.ndim == max_ndim and np.sum(obj.shape):
                    sample = obj
                    break

        else:
            # filter out the empties if we have not multi-index possibilities
            # note to keep empty Series as it affect to result columns / name
            non_empties = [obj for obj in objs if sum(obj.shape) > 0 or obj.ndim == 1]

            if len(non_empties) and (
                keys is None and names is None and levels is None and not self.intersect
            ):
                objs = non_empties
                sample = objs[0]

        if sample is None:
            sample = objs[0]
        return sample, objs
