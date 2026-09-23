    def map(self, mapper):
        """
        Map categories using input correspondence (dict, Series, or function).

        Parameters
        ----------
        mapper : dict, Series, callable
            The correspondence from old values to new.

        Returns
        -------
        SparseArray
            The output array will have the same density as the input.
            The output fill value will be the result of applying the
            mapping to ``self.fill_value``

        Examples
        --------
        >>> arr = pd.SparseArray([0, 1, 2])
        >>> arr.apply(lambda x: x + 10)
        [10, 11, 12]
        Fill: 10
        IntIndex
        Indices: array([1, 2], dtype=int32)

        >>> arr.apply({0: 10, 1: 11, 2: 12})
        [10, 11, 12]
        Fill: 10
        IntIndex
        Indices: array([1, 2], dtype=int32)

        >>> arr.apply(pd.Series([10, 11, 12], index=[0, 1, 2]))
        [10, 11, 12]
        Fill: 10
        IntIndex
        Indices: array([1, 2], dtype=int32)
        """
        # this is used in apply.
        # We get hit since we're an "is_extension_type" but regular extension
        # types are not hit. This may be worth adding to the interface.
        if isinstance(mapper, ABCSeries):
            mapper = mapper.to_dict()

        if isinstance(mapper, compat.Mapping):
            fill_value = mapper.get(self.fill_value, self.fill_value)
            sp_values = [mapper.get(x, None) for x in self.sp_values]
        else:
            fill_value = mapper(self.fill_value)
            sp_values = [mapper(x) for x in self.sp_values]

        return type(self)(sp_values, sparse_index=self.sp_index,
                          fill_value=fill_value)
