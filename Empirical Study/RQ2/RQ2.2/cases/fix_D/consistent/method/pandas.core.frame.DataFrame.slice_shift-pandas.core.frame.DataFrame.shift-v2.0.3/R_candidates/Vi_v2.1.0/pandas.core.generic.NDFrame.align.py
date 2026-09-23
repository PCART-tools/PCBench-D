    @final
    @doc(
        klass=_shared_doc_kwargs["klass"],
        axes_single_arg=_shared_doc_kwargs["axes_single_arg"],
    )
    def align(
        self,
        other: NDFrameT,
        join: AlignJoin = "outer",
        axis: Axis | None = None,
        level: Level | None = None,
        copy: bool_t | None = None,
        fill_value: Hashable | None = None,
        method: FillnaOptions | None | lib.NoDefault = lib.no_default,
        limit: int | None | lib.NoDefault = lib.no_default,
        fill_axis: Axis | lib.NoDefault = lib.no_default,
        broadcast_axis: Axis | None | lib.NoDefault = lib.no_default,
    ) -> tuple[Self, NDFrameT]:
        """
        Align two objects on their axes with the specified join method.

        Join method is specified for each axis Index.

        Parameters
        ----------
        other : DataFrame or Series
        join : {{'outer', 'inner', 'left', 'right'}}, default 'outer'
            Type of alignment to be performed.

            * left: use only keys from left frame, preserve key order.
            * right: use only keys from right frame, preserve key order.
            * outer: use union of keys from both frames, sort keys lexicographically.
            * inner: use intersection of keys from both frames,
              preserve the order of the left keys.

        axis : allowed axis of the other object, default None
            Align on index (0), columns (1), or both (None).
        level : int or level name, default None
            Broadcast across a level, matching Index values on the
            passed MultiIndex level.
        copy : bool, default True
            Always returns new objects. If copy=False and no reindexing is
            required then original objects are returned.
        fill_value : scalar, default np.nan
            Value to use for missing values. Defaults to NaN, but can be any
            "compatible" value.
        method : {{'backfill', 'bfill', 'pad', 'ffill', None}}, default None
            Method to use for filling holes in reindexed Series:

            - pad / ffill: propagate last valid observation forward to next valid.
            - backfill / bfill: use NEXT valid observation to fill gap.

            .. deprecated:: 2.1

        limit : int, default None
            If method is specified, this is the maximum number of consecutive
            NaN values to forward/backward fill. In other words, if there is
            a gap with more than this number of consecutive NaNs, it will only
            be partially filled. If method is not specified, this is the
            maximum number of entries along the entire axis where NaNs will be
            filled. Must be greater than 0 if not None.

            .. deprecated:: 2.1

        fill_axis : {axes_single_arg}, default 0
            Filling axis, method and limit.

            .. deprecated:: 2.1

        broadcast_axis : {axes_single_arg}, default None
            Broadcast values along this axis, if aligning two objects of
            different dimensions.

            .. deprecated:: 2.1

        Returns
        -------
        tuple of ({klass}, type of other)
            Aligned objects.

        Examples
        --------
        >>> df = pd.DataFrame(
        ...     [[1, 2, 3, 4], [6, 7, 8, 9]], columns=["D", "B", "E", "A"], index=[1, 2]
        ... )
        >>> other = pd.DataFrame(
        ...     [[10, 20, 30, 40], [60, 70, 80, 90], [600, 700, 800, 900]],
        ...     columns=["A", "B", "C", "D"],
        ...     index=[2, 3, 4],
        ... )
        >>> df
           D  B  E  A
        1  1  2  3  4
        2  6  7  8  9
        >>> other
            A    B    C    D
        2   10   20   30   40
        3   60   70   80   90
        4  600  700  800  900

        Align on columns:

        >>> left, right = df.align(other, join="outer", axis=1)
        >>> left
           A  B   C  D  E
        1  4  2 NaN  1  3
        2  9  7 NaN  6  8
        >>> right
            A    B    C    D   E
        2   10   20   30   40 NaN
        3   60   70   80   90 NaN
        4  600  700  800  900 NaN

        We can also align on the index:

        >>> left, right = df.align(other, join="outer", axis=0)
        >>> left
            D    B    E    A
        1  1.0  2.0  3.0  4.0
        2  6.0  7.0  8.0  9.0
        3  NaN  NaN  NaN  NaN
        4  NaN  NaN  NaN  NaN
        >>> right
            A      B      C      D
        1    NaN    NaN    NaN    NaN
        2   10.0   20.0   30.0   40.0
        3   60.0   70.0   80.0   90.0
        4  600.0  700.0  800.0  900.0

        Finally, the default `axis=None` will align on both index and columns:

        >>> left, right = df.align(other, join="outer", axis=None)
        >>> left
             A    B   C    D    E
        1  4.0  2.0 NaN  1.0  3.0
        2  9.0  7.0 NaN  6.0  8.0
        3  NaN  NaN NaN  NaN  NaN
        4  NaN  NaN NaN  NaN  NaN
        >>> right
               A      B      C      D   E
        1    NaN    NaN    NaN    NaN NaN
        2   10.0   20.0   30.0   40.0 NaN
        3   60.0   70.0   80.0   90.0 NaN
        4  600.0  700.0  800.0  900.0 NaN
        """
        if (
            method is not lib.no_default
            or limit is not lib.no_default
            or fill_axis is not lib.no_default
        ):
            # GH#51856
            warnings.warn(
                "The 'method', 'limit', and 'fill_axis' keywords in "
                f"{type(self).__name__}.align are deprecated and will be removed "
                "in a future version. Call fillna directly on the returned objects "
                "instead.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        if fill_axis is lib.no_default:
            fill_axis = 0
        if method is lib.no_default:
            method = None
        if limit is lib.no_default:
            limit = None

        if method is not None:
            method = clean_fill_method(method)

        if broadcast_axis is not lib.no_default:
            # GH#51856
            # TODO(3.0): enforcing this deprecation will close GH#13194
            msg = (
                f"The 'broadcast_axis' keyword in {type(self).__name__}.align is "
                "deprecated and will be removed in a future version."
            )
            if broadcast_axis is not None:
                if self.ndim == 1 and other.ndim == 2:
                    msg += (
                        " Use left = DataFrame({col: left for col in right.columns}, "
                        "index=right.index) before calling `left.align(right)` instead."
                    )
                elif self.ndim == 2 and other.ndim == 1:
                    msg += (
                        " Use right = DataFrame({col: right for col in left.columns}, "
                        "index=left.index) before calling `left.align(right)` instead"
                    )
            warnings.warn(msg, FutureWarning, stacklevel=find_stack_level())
        else:
            broadcast_axis = None

        if broadcast_axis == 1 and self.ndim != other.ndim:
            if isinstance(self, ABCSeries):
                # this means other is a DataFrame, and we need to broadcast
                # self
                cons = self._constructor_expanddim
                df = cons(
                    {c: self for c in other.columns}, **other._construct_axes_dict()
                )
                # error: Incompatible return value type (got "Tuple[DataFrame,
                # DataFrame]", expected "Tuple[Self, NDFrameT]")
                return df._align_frame(  # type: ignore[return-value]
                    other,  # type: ignore[arg-type]
                    join=join,
                    axis=axis,
                    level=level,
                    copy=copy,
                    fill_value=fill_value,
                    method=method,
                    limit=limit,
                    fill_axis=fill_axis,
                )[:2]
            elif isinstance(other, ABCSeries):
                # this means self is a DataFrame, and we need to broadcast
                # other
                cons = other._constructor_expanddim
                df = cons(
                    {c: other for c in self.columns}, **self._construct_axes_dict()
                )
                # error: Incompatible return value type (got "Tuple[NDFrameT,
                # DataFrame]", expected "Tuple[Self, NDFrameT]")
                return self._align_frame(  # type: ignore[return-value]
                    df,
                    join=join,
                    axis=axis,
                    level=level,
                    copy=copy,
                    fill_value=fill_value,
                    method=method,
                    limit=limit,
                    fill_axis=fill_axis,
                )[:2]

        _right: DataFrame | Series
        if axis is not None:
            axis = self._get_axis_number(axis)
        if isinstance(other, ABCDataFrame):
            left, _right, join_index = self._align_frame(
                other,
                join=join,
                axis=axis,
                level=level,
                copy=copy,
                fill_value=fill_value,
                method=method,
                limit=limit,
                fill_axis=fill_axis,
            )

        elif isinstance(other, ABCSeries):
            left, _right, join_index = self._align_series(
                other,
                join=join,
                axis=axis,
                level=level,
                copy=copy,
                fill_value=fill_value,
                method=method,
                limit=limit,
                fill_axis=fill_axis,
            )
        else:  # pragma: no cover
            raise TypeError(f"unsupported type: {type(other)}")

        right = cast(NDFrameT, _right)
        if self.ndim == 1 or axis == 0:
            # If we are aligning timezone-aware DatetimeIndexes and the timezones
            #  do not match, convert both to UTC.
            if isinstance(left.index.dtype, DatetimeTZDtype):
                if left.index.tz != right.index.tz:
                    if join_index is not None:
                        # GH#33671 copy to ensure we don't change the index on
                        #  our original Series
                        left = left.copy(deep=False)
                        right = right.copy(deep=False)
                        left.index = join_index
                        right.index = join_index

        left = left.__finalize__(self)
        right = right.__finalize__(other)
        return left, right
