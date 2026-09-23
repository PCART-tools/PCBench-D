    def to_series(self, keep_tz=False, index=None, name=None):
        """
        Create a Series with both index and values equal to the index keys
        useful with map for returning an indexer based on an index

        Parameters
        ----------
        keep_tz : optional, defaults False.
            return the data keeping the timezone.

            If keep_tz is True:

              If the timezone is not set, the resulting
              Series will have a datetime64[ns] dtype.

              Otherwise the Series will have an datetime64[ns, tz] dtype; the
              tz will be preserved.

            If keep_tz is False:

              Series will have a datetime64[ns] dtype. TZ aware
              objects will have the tz removed.
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

        return Series(self._to_embed(keep_tz), index=index, name=name)
