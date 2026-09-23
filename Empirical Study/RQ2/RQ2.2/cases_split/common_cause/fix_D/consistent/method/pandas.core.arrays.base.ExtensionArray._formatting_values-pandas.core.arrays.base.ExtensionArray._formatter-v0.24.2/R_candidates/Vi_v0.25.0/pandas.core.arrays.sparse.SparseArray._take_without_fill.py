    def _take_without_fill(self, indices):
        to_shift = indices < 0
        indices = indices.copy()

        n = len(self)

        if (indices.max() >= n) or (indices.min() < -n):
            if n == 0:
                raise IndexError("cannot do a non-empty take from an " "empty axes.")
            else:
                raise IndexError("out of bounds value in 'indices'.")

        if to_shift.any():
            indices[to_shift] += n

        if self.sp_index.npoints == 0:
            # edge case in take...
            # I think just return
            out = np.full(
                indices.shape,
                self.fill_value,
                dtype=np.result_type(type(self.fill_value)),
            )
            arr, sp_index, fill_value = make_sparse(out, fill_value=self.fill_value)
            return type(self)(arr, sparse_index=sp_index, fill_value=fill_value)

        sp_indexer = self.sp_index.lookup_array(indices)
        taken = self.sp_values.take(sp_indexer)
        fillable = sp_indexer < 0

        if fillable.any():
            # TODO: may need to coerce array to fill value
            result_type = np.result_type(taken, type(self.fill_value))
            taken = taken.astype(result_type)
            taken[fillable] = self.fill_value

        return taken
