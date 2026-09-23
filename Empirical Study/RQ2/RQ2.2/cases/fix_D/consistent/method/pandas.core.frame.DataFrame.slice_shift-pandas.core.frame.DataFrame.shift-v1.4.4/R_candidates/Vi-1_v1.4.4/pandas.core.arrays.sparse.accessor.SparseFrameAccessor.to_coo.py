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

        dtype = find_common_type(self._parent.dtypes.to_list())
        if isinstance(dtype, SparseDtype):
            dtype = dtype.subtype

        cols, rows, data = [], [], []
        for col, (_, ser) in enumerate(self._parent.iteritems()):
            sp_arr = ser.array
            if sp_arr.fill_value != 0:
                raise ValueError("fill value must be 0 when converting to COO matrix")

            row = sp_arr.sp_index.indices
            cols.append(np.repeat(col, len(row)))
            rows.append(row)
            data.append(sp_arr.sp_values.astype(dtype, copy=False))

        cols = np.concatenate(cols)
        rows = np.concatenate(rows)
        data = np.concatenate(data)
        return coo_matrix((data, (rows, cols)), shape=self._parent.shape)
