    @staticmethod
    def from_imperative(value):
        """ Create bag item from an imperative value

        Parameters
        ----------
        value: a Value
            A single dask.imperative.Value object, such as come from dask.do

        Returns
        -------
        Item

        Examples
        --------
        >>> b = db.Item.from_imperative(x)  # doctest: +SKIP
        """
        from dask.imperative import Value
        assert isinstance(value, Value)
        return Item(value.dask, value.key)
