    def to_series(self, keep_tz=lib.no_default, index=None, name=None):
        """
        Create a Series with both index and values equal to the index keys.

        Useful with map for returning an indexer based on an index.

        Parameters
        ----------
        keep_tz : optional, defaults True
            Return the data keeping the timezone.

            If keep_tz is True:

              If the timezone is not set, the resulting
              Series will have a datetime64[ns] dtype.

              Otherwise the Series will have an datetime64[ns, tz] dtype; the
              tz will be preserved.

            If keep_tz is False:

              Series will have a datetime64[ns] dtype. TZ aware
              objects will have the tz removed.

            .. versionchanged:: 1.0.0
                The default value is now True.  In a future version,
                this keyword will be removed entirely.  Stop passing the
                argument to obtain the future behavior and silence the warning.

        index : Index, optional
            Index of resulting Series. If None, defaults to original index.
        name : str, optional
            Name of resulting Series. If None, defaults to name of original
            index.

        Returns
        -------
        Series
        """
        from pandas import Series

        if index is None:
            index = self._view()
        if name is None:
            name = self.name

        if keep_tz is not lib.no_default:
            if keep_tz:
                warnings.warn(
                    "The 'keep_tz' keyword in DatetimeIndex.to_series "
                    "is deprecated and will be removed in a future version. "
                    "You can stop passing 'keep_tz' to silence this warning.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
            else:
                warnings.warn(
                    "Specifying 'keep_tz=False' is deprecated and this "
                    "option will be removed in a future release. If "
                    "you want to remove the timezone information, you "
                    "can do 'idx.tz_convert(None)' before calling "
                    "'to_series'.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
        else:
            keep_tz = True

        if keep_tz and self.tz is not None:
            # preserve the tz & copy
            values = self.copy(deep=True)
        else:
            # error: Incompatible types in assignment (expression has type
            # "Union[ExtensionArray, ndarray]", variable has type "DatetimeIndex")
            values = self._values.view("M8[ns]").copy()  # type: ignore[assignment]

        return Series(values, index=index, name=name)
