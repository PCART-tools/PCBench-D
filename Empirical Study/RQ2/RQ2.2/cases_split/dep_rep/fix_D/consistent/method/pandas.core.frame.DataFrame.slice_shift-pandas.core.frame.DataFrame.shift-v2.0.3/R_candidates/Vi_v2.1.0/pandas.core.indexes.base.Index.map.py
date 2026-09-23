    def map(self, mapper, na_action: Literal["ignore"] | None = None):
        """
        Map values using an input mapping or function.

        Parameters
        ----------
        mapper : function, dict, or Series
            Mapping correspondence.
        na_action : {None, 'ignore'}
            If 'ignore', propagate NA values, without passing them to the
            mapping correspondence.

        Returns
        -------
        Union[Index, MultiIndex]
            The output of the mapping function applied to the index.
            If the function returns a tuple with more than one element
            a MultiIndex will be returned.

        Examples
        --------
        >>> idx = pd.Index([1, 2, 3])
        >>> idx.map({1: 'a', 2: 'b', 3: 'c'})
        Index(['a', 'b', 'c'], dtype='object')

        Using `map` with a function:

        >>> idx = pd.Index([1, 2, 3])
        >>> idx.map('I am a {}'.format)
        Index(['I am a 1', 'I am a 2', 'I am a 3'], dtype='object')

        >>> idx = pd.Index(['a', 'b', 'c'])
        >>> idx.map(lambda x: x.upper())
        Index(['A', 'B', 'C'], dtype='object')
        """
        from pandas.core.indexes.multi import MultiIndex

        new_values = self._map_values(mapper, na_action=na_action)

        # we can return a MultiIndex
        if new_values.size and isinstance(new_values[0], tuple):
            if isinstance(self, MultiIndex):
                names = self.names
            elif self.name:
                names = [self.name] * len(new_values[0])
            else:
                names = None
            return MultiIndex.from_tuples(new_values, names=names)

        dtype = None
        if not new_values.size:
            # empty
            dtype = self.dtype

        # e.g. if we are floating and new_values is all ints, then we
        #  don't want to cast back to floating.  But if we are UInt64
        #  and new_values is all ints, we want to try.
        same_dtype = lib.infer_dtype(new_values, skipna=False) == self.inferred_type
        if same_dtype:
            new_values = maybe_cast_pointwise_result(
                new_values, self.dtype, same_dtype=same_dtype
            )

        return Index._with_infer(new_values, dtype=dtype, copy=False, name=self.name)
