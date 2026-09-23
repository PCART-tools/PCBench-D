    @staticmethod
    def _extract_axis(self, data, axis=0, intersect=False):

        index = None
        if len(data) == 0:
            index = Index([])
        elif len(data) > 0:
            raw_lengths = []

        have_raw_arrays = False
        have_frames = False

        for v in data.values():
            if isinstance(v, self._constructor_sliced):
                have_frames = True
            elif v is not None:
                have_raw_arrays = True
                raw_lengths.append(v.shape[axis])

        if have_frames:
            # we want the "old" behavior here, of sorting only
            # 1. we're doing a union (intersect=False)
            # 2. the indices are not aligned.
            index = _get_objs_combined_axis(data.values(), axis=axis,
                                            intersect=intersect, sort=None)

        if have_raw_arrays:
            lengths = list(set(raw_lengths))
            if len(lengths) > 1:
                raise ValueError('ndarrays must match shape on '
                                 'axis {ax}'.format(ax=axis))

            if have_frames:
                if lengths[0] != len(index):
                    raise AssertionError('Length of data and index must match')
            else:
                index = Index(np.arange(lengths[0]))

        if index is None:
            index = Index([])

        return ensure_index(index)
