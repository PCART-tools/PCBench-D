    @Appender(_index_shared_docs['take'] % _sparray_doc_kwargs)
    def take(self, indices, axis=0, allow_fill=True,
             fill_value=None, **kwargs):
        """
        Sparse-compatible version of ndarray.take

        Returns
        -------
        taken : ndarray
        """
        nv.validate_take(tuple(), kwargs)

        if axis:
            raise ValueError("axis must be 0, input was {0}".format(axis))

        if is_integer(indices):
            # return scalar
            return self[indices]

        indices = _ensure_platform_int(indices)
        n = len(self)
        if allow_fill and fill_value is not None:
            # allow -1 to indicate self.fill_value,
            # self.fill_value may not be NaN
            if (indices < -1).any():
                msg = ('When allow_fill=True and fill_value is not None, '
                       'all indices must be >= -1')
                raise ValueError(msg)
            elif (n <= indices).any():
                msg = 'index is out of bounds for size {0}'
                raise IndexError(msg.format(n))
        else:
            if ((indices < -n) | (n <= indices)).any():
                msg = 'index is out of bounds for size {0}'
                raise IndexError(msg.format(n))

        indices = indices.astype(np.int32)
        if not (allow_fill and fill_value is not None):
            indices = indices.copy()
            indices[indices < 0] += n

        locs = self.sp_index.lookup_array(indices)
        indexer = np.arange(len(locs), dtype=np.int32)
        mask = locs != -1
        if mask.any():
            indexer = indexer[mask]
            new_values = self.sp_values.take(locs[mask])
        else:
            indexer = np.empty(shape=(0, ), dtype=np.int32)
            new_values = np.empty(shape=(0, ), dtype=self.sp_values.dtype)

        sp_index = _make_index(len(indices), indexer, kind=self.sp_index)
        return self._simple_new(new_values, sp_index, self.fill_value)
