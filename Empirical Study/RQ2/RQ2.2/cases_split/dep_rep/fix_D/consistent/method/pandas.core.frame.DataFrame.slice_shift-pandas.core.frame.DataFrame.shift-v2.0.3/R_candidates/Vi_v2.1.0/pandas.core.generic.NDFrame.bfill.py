    @final
    @doc(
        klass=_shared_doc_kwargs["klass"],
        axes_single_arg=_shared_doc_kwargs["axes_single_arg"],
    )
    def bfill(
        self,
        *,
        axis: None | Axis = None,
        inplace: bool_t = False,
        limit: None | int = None,
        downcast: dict | None | lib.NoDefault = lib.no_default,
    ) -> Self | None:
        """
        Fill NA/NaN values by using the next valid observation to fill the gap.

        Parameters
        ----------
        axis : {axes_single_arg}
            Axis along which to fill missing values. For `Series`
            this parameter is unused and defaults to 0.
        inplace : bool, default False
            If True, fill in-place. Note: this will modify any
            other views on this object (e.g., a no-copy slice for a column in a
            DataFrame).
        limit : int, default None
            If method is specified, this is the maximum number of consecutive
            NaN values to forward/backward fill. In other words, if there is
            a gap with more than this number of consecutive NaNs, it will only
            be partially filled. If method is not specified, this is the
            maximum number of entries along the entire axis where NaNs will be
            filled. Must be greater than 0 if not None.
        downcast : dict, default is None
            A dict of item->dtype of what to downcast if possible,
            or the string 'infer' which will try to downcast to an appropriate
            equal type (e.g. float64 to int64 if possible).

        Returns
        -------
        {klass} or None
            Object with missing values filled or None if ``inplace=True``.

        Examples
        --------
        For Series:

        >>> s = pd.Series([1, None, None, 2])
        >>> s.bfill()
        0    1.0
        1    2.0
        2    2.0
        3    2.0
        dtype: float64
        >>> s.bfill(limit=1)
        0    1.0
        1    NaN
        2    2.0
        3    2.0
        dtype: float64

        With DataFrame:

        >>> df = pd.DataFrame({{'A': [1, None, None, 4], 'B': [None, 5, None, 7]}})
        >>> df
              A     B
        0   1.0	  NaN
        1   NaN	  5.0
        2   NaN   NaN
        3   4.0   7.0
        >>> df.bfill()
              A     B
        0   1.0   5.0
        1   4.0   5.0
        2   4.0   7.0
        3   4.0   7.0
        >>> df.bfill(limit=1)
              A     B
        0   1.0   5.0
        1   NaN   5.0
        2   4.0   7.0
        3   4.0   7.0
        """
        downcast = self._deprecate_downcast(downcast, "bfill")
        inplace = validate_bool_kwarg(inplace, "inplace")
        if inplace:
            if not PYPY and using_copy_on_write():
                if sys.getrefcount(self) <= REF_COUNT:
                    warnings.warn(
                        _chained_assignment_method_msg,
                        ChainedAssignmentError,
                        stacklevel=2,
                    )
        return self._pad_or_backfill(
            "bfill",
            axis=axis,
            inplace=inplace,
            limit=limit,
            # error: Argument "downcast" to "_fillna_with_method" of "NDFrame"
            # has incompatible type "Union[Dict[Any, Any], None,
            # Literal[_NoDefault.no_default]]"; expected "Optional[Dict[Any, Any]]"
            downcast=downcast,  # type: ignore[arg-type]
        )
