    def as_sparse_array(self, kind=None, fill_value=None, copy=False):
        """ return my self as a sparse array, do not copy by default """

        if fill_value is None:
            fill_value = self.fill_value
        if kind is None:
            kind = self.kind
        return SparseArray(
            self.values,
            sparse_index=self.sp_index,
            fill_value=fill_value,
            kind=kind,
            copy=copy,
        )
