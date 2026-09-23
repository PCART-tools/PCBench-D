    def astype(self, dtype: AstypeArg | None = None, copy: bool = True):
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
        if is_dtype_equal(dtype, self._dtype):
            if not copy:
                return self
            else:
                return self.copy()
        dtype = self.dtype.update_dtype(dtype)
        subtype = pandas_dtype(dtype._subtype_with_str)
        sp_values = astype_nansafe(self.sp_values, subtype, copy=copy)

        # error: Argument 1 to "_simple_new" of "SparseArray" has incompatible type
        # "ExtensionArray"; expected "ndarray"
        return self._simple_new(
            sp_values, self.sp_index, dtype  # type: ignore[arg-type]
        )
