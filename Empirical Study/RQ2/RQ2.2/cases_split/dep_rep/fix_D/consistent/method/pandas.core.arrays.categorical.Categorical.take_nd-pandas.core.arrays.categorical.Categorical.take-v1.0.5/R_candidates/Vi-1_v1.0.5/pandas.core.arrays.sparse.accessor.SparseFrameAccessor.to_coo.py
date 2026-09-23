    def to_coo(self):
        """
        Return the contents of the frame as a sparse SciPy COO matrix.

        .. versionadded:: 0.25.0

        Returns
        -------
        coo_matrix : scipy.sparse.spmatrix
            If the caller is heterogeneous and contains booleans or objects,
            the result will be of dtype=object. See Notes.

        Notes
        -----
        The dtype will be the lowest-common-denominator type (implicit
        upcasting); that is to say if the dtypes (even of numeric types)
        are mixed, the one that accommodates all will be chosen.

        e.g. If the dtypes are float16 and float32, dtype will be upcast to
        float32. By numpy.find_common_type convention, mixing int64 and
        and uint64 will result in a float64 dtype.
        """
        import_optional_dependency("scipy")
        from scipy.sparse import coo_matrix

        dtype = find_common_type(self._parent.dtypes)
        if isinstance(dtype, SparseDtype):
            dtype = dtype.subtype

        cols, rows, datas = [], [], []
        for col, name in enumerate(self._parent):
            s = self._parent[name]
            row = s.array.sp_index.to_int_index().indices
            cols.append(np.repeat(col, len(row)))
            rows.append(row)
            datas.append(s.array.sp_values.astype(dtype, copy=False))

        cols = np.concatenate(cols)
        rows = np.concatenate(rows)
        datas = np.concatenate(datas)
        return coo_matrix((datas, (rows, cols)), shape=self._parent.shape)
