    def take(self, indices, axis=0, convert=True, *args, **kwargs):
        """
        Sparse-compatible version of ndarray.take

        Returns
        -------
        taken : ndarray
        """

        convert = nv.validate_take_with_convert(convert, args, kwargs)
        new_values = SparseArray.take(self.values, indices)
        new_index = self.index.take(indices)
        return self._constructor(new_values,
                                 index=new_index).__finalize__(self)
