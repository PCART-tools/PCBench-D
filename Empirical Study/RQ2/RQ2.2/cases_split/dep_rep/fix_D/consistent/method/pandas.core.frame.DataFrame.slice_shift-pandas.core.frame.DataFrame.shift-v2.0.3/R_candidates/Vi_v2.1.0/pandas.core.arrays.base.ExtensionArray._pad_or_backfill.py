    def _pad_or_backfill(
        self, *, method: FillnaOptions, limit: int | None = None, copy: bool = True
    ) -> Self:
        """
        Pad or backfill values, used by Series/DataFrame ffill and bfill.

        Parameters
        ----------
        method : {'backfill', 'bfill', 'pad', 'ffill'}
            Method to use for filling holes in reindexed Series:

            * pad / ffill: propagate last valid observation forward to next valid.
            * backfill / bfill: use NEXT valid observation to fill gap.

        limit : int, default None
            This is the maximum number of consecutive
            NaN values to forward/backward fill. In other words, if there is
            a gap with more than this number of consecutive NaNs, it will only
            be partially filled. If method is not specified, this is the
            maximum number of entries along the entire axis where NaNs will be
            filled.

        copy : bool, default True
            Whether to make a copy of the data before filling. If False, then
            the original should be modified and no new memory should be allocated.
            For ExtensionArray subclasses that cannot do this, it is at the
            author's discretion whether to ignore "copy=False" or to raise.
            The base class implementation ignores the keyword if any NAs are
            present.

        Returns
        -------
        Same type as self

        Examples
        --------
        >>> arr = pd.array([np.nan, np.nan, 2, 3, np.nan, np.nan])
        >>> arr._pad_or_backfill(method="backfill", limit=1)
        <IntegerArray>
        [<NA>, 2, 2, 3, <NA>, <NA>]
        Length: 6, dtype: Int64
        """

        # If a 3rd-party EA has implemented this functionality in fillna,
        #  we warn that they need to implement _pad_or_backfill instead.
        if (
            type(self).fillna is not ExtensionArray.fillna
            and type(self)._pad_or_backfill is ExtensionArray._pad_or_backfill
        ):
            # Check for _pad_or_backfill here allows us to call
            #  super()._pad_or_backfill without getting this warning
            warnings.warn(
                "ExtensionArray.fillna 'method' keyword is deprecated. "
                "In a future version. arr._pad_or_backfill will be called "
                "instead. 3rd-party ExtensionArray authors need to implement "
                "_pad_or_backfill.",
                DeprecationWarning,
                stacklevel=find_stack_level(),
            )
            return self.fillna(method=method, limit=limit)

        mask = self.isna()

        if mask.any():
            # NB: the base class does not respect the "copy" keyword
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
            if not copy:
                return self
            new_values = self.copy()
        return new_values
