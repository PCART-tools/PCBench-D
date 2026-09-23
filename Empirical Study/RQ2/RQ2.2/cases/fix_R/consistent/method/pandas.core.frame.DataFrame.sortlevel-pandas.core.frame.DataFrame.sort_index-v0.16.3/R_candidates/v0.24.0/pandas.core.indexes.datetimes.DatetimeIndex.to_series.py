    def to_series(self, keep_tz=None, index=None, name=None):
        """
        Create a Series with both index and values equal to the index keys
        useful with map for returning an indexer based on an index

        Parameters
        ----------
        keep_tz : optional, defaults False
            Return the data keeping the timezone.

            If keep_tz is True:

              If the timezone is not set, the resulting
              Series will have a datetime64[ns] dtype.

              Otherwise the Series will have an datetime64[ns, tz] dtype; the
              tz will be preserved.

            If keep_tz is False:

              Series will have a datetime64[ns] dtype. TZ aware
              objects will have the tz removed.

            .. versionchanged:: 0.24
                The default value will change to True in a future release.
                You can set ``keep_tz=True`` to already obtain the future
                behaviour and silence the warning.

        index : Index, optional
            index of resulting Series. If None, defaults to original index
        name : string, optional
            name of resulting Series. If None, defaults to name of original
            index

        Returns
        -------
        Series
        """
        from pandas import Series

        if index is None:
            index = self._shallow_copy()
        if name is None:
            name = self.name

        if keep_tz is None and self.tz is not None:
            warnings.warn("The default of the 'keep_tz' keyword will change "
                          "to True in a future release. You can set "
                          "'keep_tz=True' to obtain the future behaviour and "
                          "silence this warning.", FutureWarning, stacklevel=2)
            keep_tz = False
        elif keep_tz is False:
            warnings.warn("Specifying 'keep_tz=False' is deprecated and this "
                          "option will be removed in a future release. If "
                          "you want to remove the timezone information, you "
                          "can do 'idx.tz_convert(None)' before calling "
                          "'to_series'.", FutureWarning, stacklevel=2)

        if keep_tz and self.tz is not None:
            # preserve the tz & copy
            values = self.copy(deep=True)
        else:
            values = self.values.copy()

        return Series(values, index=index, name=name)
