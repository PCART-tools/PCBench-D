    def _init_matrix(self, data, axes, dtype=None, copy=False):
        values = self._prep_ndarray(self, data, copy=copy)

        if dtype is not None:
            try:
                values = values.astype(dtype)
            except Exception:
                raise ValueError('failed to cast to %s' % dtype)

        shape = values.shape
        fixed_axes = []
        for i, ax in enumerate(axes):
            if ax is None:
                ax = _default_index(shape[i])
            else:
                ax = _ensure_index(ax)
            fixed_axes.append(ax)

        return create_block_manager_from_blocks([values], fixed_axes)
