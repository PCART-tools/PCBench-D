    def _align_series(self, indexer, ser):
        # indexer to assign Series can be tuple, slice, scalar
        if isinstance(indexer, (slice, np.ndarray, list)):
            indexer = tuple([indexer])

        if isinstance(indexer, tuple):

            # flatten np.ndarray indexers
            ravel = lambda i: i.ravel() if isinstance(i, np.ndarray) else i
            indexer = tuple(map(ravel, indexer))

            aligners = [not is_null_slice(idx) for idx in indexer]
            sum_aligners = sum(aligners)
            single_aligner = sum_aligners == 1
            is_frame = self.obj.ndim == 2
            is_panel = self.obj.ndim >= 3
            obj = self.obj

            # are we a single alignable value on a non-primary
            # dim (e.g. panel: 1,2, or frame: 0) ?
            # hence need to align to a single axis dimension
            # rather that find all valid dims

            # frame
            if is_frame:
                single_aligner = single_aligner and aligners[0]

            # panel
            elif is_panel:
                single_aligner = (single_aligner and
                                  (aligners[1] or aligners[2]))

            # we have a frame, with multiple indexers on both axes; and a
            # series, so need to broadcast (see GH5206)
            if (sum_aligners == self.ndim and
                    all([com.is_sequence(_) for _ in indexer])):
                ser = ser.reindex(obj.axes[0][indexer[0]], copy=True).values

                # single indexer
                if len(indexer) > 1:
                    l = len(indexer[1])
                    ser = np.tile(ser, l).reshape(l, -1).T

                return ser

            for i, idx in enumerate(indexer):
                ax = obj.axes[i]

                # multiple aligners (or null slices)
                if com.is_sequence(idx) or isinstance(idx, slice):
                    if single_aligner and is_null_slice(idx):
                        continue
                    new_ix = ax[idx]
                    if not is_list_like_indexer(new_ix):
                        new_ix = Index([new_ix])
                    else:
                        new_ix = Index(new_ix)
                    if ser.index.equals(new_ix) or not len(new_ix):
                        return ser.values.copy()

                    return ser.reindex(new_ix).values

                # 2 dims
                elif single_aligner and is_frame:

                    # reindex along index
                    ax = self.obj.axes[1]
                    if ser.index.equals(ax) or not len(ax):
                        return ser.values.copy()
                    return ser.reindex(ax).values

                # >2 dims
                elif single_aligner:

                    broadcast = []
                    for n, labels in enumerate(self.obj._get_plane_axes(i)):

                        # reindex along the matching dimensions
                        if len(labels & ser.index):
                            ser = ser.reindex(labels)
                        else:
                            broadcast.append((n, len(labels)))

                    # broadcast along other dims
                    ser = ser.values.copy()
                    for (axis, l) in broadcast:
                        shape = [-1] * (len(broadcast) + 1)
                        shape[axis] = l
                        ser = np.tile(ser, l).reshape(shape)

                    if self.obj.ndim == 3:
                        ser = ser.T

                    return ser

        elif np.isscalar(indexer):
            ax = self.obj._get_axis(1)

            if ser.index.equals(ax):
                return ser.values.copy()

            return ser.reindex(ax).values

        raise ValueError('Incompatible indexer with Series')
