    def fillna(
        self,
        value: object | ArrayLike | None = None,
        method: FillnaOptions | None = None,
        limit: int | None = None,
        copy: bool = True,
    ) -> Self:
        """
        Fill NA/NaN values using the specified method.

        Parameters
        ----------
        value : scalar, array-like
            If a scalar value is passed it is used to fill all missing values.
            Alternatively, an array-like "value" can be given. It's expected
            that the array-like have the same length as 'self'.
        method : {'backfill', 'bfill', 'pad', 'ffill', None}, default None
            Method to use for filling holes in reindexed Series:

            * pad / ffill: propagate last valid observation forward to next valid.
            * backfill / bfill: use NEXT valid observation to fill gap.

            .. deprecated:: 2.1.0

        limit : int, default None
            If method is specified, this is the maximum number of consecutive
            NaN values to forward/backward fill. In other words, if there is
            a gap with more than this number of consecutive NaNs, it will only
            be partially filled. If method is not specified, this is the
            maximum number of entries along the entire axis where NaNs will be
            filled.

            .. deprecated:: 2.1.0

        copy : bool, default True
            Whether to make a copy of the data before filling. If False, then
            the original should be modified and no new memory should be allocated.
            For ExtensionArray subclasses that cannot do this, it is at the
            author's discretion whether to ignore "copy=False" or to raise.
            The base class implementation ignores the keyword in pad/backfill
            cases.

        Returns
        -------
        ExtensionArray
            With NA/NaN filled.

        Examples
        --------
        >>> arr = pd.array([np.nan, np.nan, 2, 3, np.nan, np.nan])
        >>> arr.fillna(0)
        <IntegerArray>
        [0, 0, 2, 3, 0, 0]
        Length: 6, dtype: Int64
        """
        if method is not None:
            warnings.warn(
                f"The 'method' keyword in {type(self).__name__}.fillna is "
                "deprecated and will be removed in a future version.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )

        value, method = validate_fillna_kwargs(value, method)

        mask = self.isna()
        # error: Argument 2 to "check_value_size" has incompatible type
        # "ExtensionArray"; expected "ndarray"
        value = missing.check_value_size(
            value, mask, len(self)  # type: ignore[arg-type]
        )

        if mask.any():
            if method is not None:
                meth = missing.clean_fill_method(method)

                npmask = np.asarray(mask)
                if meth == "pad":
                    indexer = libalgos.get_fill_indexer(npmask, limit=limit)
                    return self.take(indexer, allow_fill=True)
                else:
                    # i.e. meth == "backfill"
                    indexer = libalgos.get_fill_indexer(npmask[::-1], limit=limit)[::-1]
                    return self[::-1].take(indexer, allow_fill=True)
            else:
                # fill with value
                if not copy:
                    new_values = self[:]
                else:
                    new_values = self.copy()
                new_values[mask] = value
        else:
            if not copy:
                new_values = self[:]
            else:
                new_values = self.copy()
        return new_values
