    def _groupby_op(
        self,
        *,
        how: str,
        has_dropped_na: bool,
        min_count: int,
        ngroups: int,
        ids: npt.NDArray[np.intp],
        **kwargs,
    ) -> ArrayLike:
        """
        Dispatch GroupBy reduction or transformation operation.

        This is an *experimental* API to allow ExtensionArray authors to implement
        reductions and transformations. The API is subject to change.

        Parameters
        ----------
        how : {'any', 'all', 'sum', 'prod', 'min', 'max', 'mean', 'median',
               'median', 'var', 'std', 'sem', 'nth', 'last', 'ohlc',
               'cumprod', 'cumsum', 'cummin', 'cummax', 'rank'}
        has_dropped_na : bool
        min_count : int
        ngroups : int
        ids : np.ndarray[np.intp]
            ids[i] gives the integer label for the group that self[i] belongs to.
        **kwargs : operation-specific
            'any', 'all' -> ['skipna']
            'var', 'std', 'sem' -> ['ddof']
            'cumprod', 'cumsum', 'cummin', 'cummax' -> ['skipna']
            'rank' -> ['ties_method', 'ascending', 'na_option', 'pct']

        Returns
        -------
        np.ndarray or ExtensionArray
        """
        from pandas.core.arrays.string_ import StringDtype
        from pandas.core.groupby.ops import WrappedCythonOp

        kind = WrappedCythonOp.get_kind_from_how(how)
        op = WrappedCythonOp(how=how, kind=kind, has_dropped_na=has_dropped_na)

        # GH#43682
        if isinstance(self.dtype, StringDtype):
            # StringArray
            npvalues = self.to_numpy(object, na_value=np.nan)
        else:
            raise NotImplementedError(
                f"function is not implemented for this dtype: {self.dtype}"
            )

        res_values = op._cython_op_ndim_compat(
            npvalues,
            min_count=min_count,
            ngroups=ngroups,
            comp_ids=ids,
            mask=None,
            **kwargs,
        )

        if op.how in op.cast_blocklist:
            # i.e. how in ["rank"], since other cast_blocklist methods don't go
            #  through cython_operation
            return res_values

        if isinstance(self.dtype, StringDtype):
            dtype = self.dtype
            string_array_cls = dtype.construct_array_type()
            return string_array_cls._from_sequence(res_values, dtype=dtype)

        else:
            raise NotImplementedError
