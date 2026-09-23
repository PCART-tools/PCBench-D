    def _update_path(self):
        if np.isnan(np.sum(self._edges)):
            raise ValueError('Nan values in "edges" are disallowed')
        if self._edges.size - 1 != self._values.size:
            raise ValueError('Size mismatch between "values" and "edges". '
                             "Expected `len(values) + 1 == len(edges)`, but "
                             f"`len(values) = {self._values.size}` and "
                             f"`len(edges) = {self._edges.size}`.")
        # Initializing with empty arrays allows supporting empty stairs.
        verts, codes = [np.empty((0, 2))], [np.empty(0, dtype=Path.code_type)]

        _nan_mask = np.isnan(self._values)
        if self._baseline is not None:
            _nan_mask |= np.isnan(self._baseline)
        for idx0, idx1 in cbook.contiguous_regions(~_nan_mask):
            x = np.repeat(self._edges[idx0:idx1+1], 2)
            y = np.repeat(self._values[idx0:idx1], 2)
            if self._baseline is None:
                y = np.concatenate([y[:1], y, y[-1:]])
            elif self._baseline.ndim == 0:  # single baseline value
                y = np.concatenate([[self._baseline], y, [self._baseline]])
            elif self._baseline.ndim == 1:  # baseline array
                base = np.repeat(self._baseline[idx0:idx1], 2)[::-1]
                x = np.concatenate([x, x[::-1]])
                y = np.concatenate([base[-1:], y, base[:1],
                                    base[:1], base, base[-1:]])
            else:  # no baseline
                raise ValueError('Invalid `baseline` specified')
            if self.orientation == 'vertical':
                xy = np.column_stack([x, y])
            else:
                xy = np.column_stack([y, x])
            verts.append(xy)
            codes.append([Path.MOVETO] + [Path.LINETO]*(len(xy)-1))
        self._path = Path(np.concatenate(verts), np.concatenate(codes))
