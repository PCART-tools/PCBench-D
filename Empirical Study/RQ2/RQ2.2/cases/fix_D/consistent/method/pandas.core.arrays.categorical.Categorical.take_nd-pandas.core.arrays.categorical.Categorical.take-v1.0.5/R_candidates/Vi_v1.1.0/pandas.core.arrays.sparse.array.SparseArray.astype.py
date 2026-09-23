    def astype(self, dtype=None, copy=True):
        """
        Change the dtype of a SparseArray.

        The output will always be a SparseArray. To convert to a dense
        ndarray with a certain dtype, use :meth:`numpy.asarray`.

        Parameters
        ----------
        dtype : np.dtype or ExtensionDtype
            For SparseDtype, this changes the dtype of
            ``self.sp_values`` and the ``self.fill_value``.

            For other dtypes, this only changes the dtype of
            ``self.sp_values``.

        copy : bool, default True
            Whether to ensure a copy is made, even if not necessary.

        Returns
        -------
        SparseArray

        Examples
        --------
        >>> arr = pd.arrays.SparseArray([0, 0, 1, 2])
        >>> arr
        [0, 0, 1, 2]
        Fill: 0
        IntIndex
        Indices: array([2, 3], dtype=int32)

        >>> arr.astype(np.dtype('int32'))
        [0, 0, 1, 2]
        Fill: 0
        IntIndex
        Indices: array([2, 3], dtype=int32)

        Using a NumPy dtype with a different kind (e.g. float) will coerce
        just ``self.sp_values``.

        >>> arr.astype(np.dtype('float64'))
        ... # doctest: +NORMALIZE_WHITESPACE
        [0.0, 0.0, 1.0, 2.0]
        Fill: 0.0
        IntIndex
        Indices: array([2, 3], dtype=int32)

        Use a SparseDtype if you wish to be change the fill value as well.

        >>> arr.astype(SparseDtype("float64", fill_value=np.nan))
        ... # doctest: +NORMALIZE_WHITESPACE
        [nan, nan, 1.0, 2.0]
        Fill: nan
        IntIndex
        Indices: array([2, 3], dtype=int32)
        """
        dtype = self.dtype.update_dtype(dtype)
        subtype = dtype._subtype_with_str
        # TODO copy=False is broken for astype_nansafe with int -> float, so cannot
        # passthrough copy keyword: https://github.com/pandas-dev/pandas/issues/34456
        sp_values = astype_nansafe(self.sp_values, subtype, copy=True)
        if sp_values is self.sp_values and copy:
            sp_values = sp_values.copy()

        return self._simple_new(sp_values, self.sp_index, dtype)
