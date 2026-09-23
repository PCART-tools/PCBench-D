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
            index = _get_objs_combined_axis(data.values(), axis=axis,
                                            intersect=intersect)

        if have_raw_arrays:
            lengths = list(set(raw_lengths))
            if len(lengths) > 1:
                raise ValueError('ndarrays must match shape on axis %d' % axis)

            if have_frames:
                if lengths[0] != len(index):
                    raise AssertionError('Length of data and index must match')
            else:
                index = Index(np.arange(lengths[0]))

        if index is None:
            index = Index([])

        return _ensure_index(index)
