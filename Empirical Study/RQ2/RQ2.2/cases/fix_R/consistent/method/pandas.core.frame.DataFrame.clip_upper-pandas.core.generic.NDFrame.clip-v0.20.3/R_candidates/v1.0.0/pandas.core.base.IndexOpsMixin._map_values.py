    def _map_values(self, mapper, na_action=None):
        """
        An internal function that maps values using the input
        correspondence (which can be a dict, Series, or function).

        Parameters
        ----------
        mapper : function, dict, or Series
            The input correspondence object
        na_action : {None, 'ignore'}
            If 'ignore', propagate NA values, without passing them to the
            mapping function

        Returns
        -------
        Union[Index, MultiIndex], inferred
            The output of the mapping function applied to the index.
            If the function returns a tuple with more than one element
            a MultiIndex will be returned.

        """

        # we can fastpath dict/Series to an efficient map
        # as we know that we are not going to have to yield
        # python types
        if is_dict_like(mapper):
            if isinstance(mapper, dict) and hasattr(mapper, "__missing__"):
                # If a dictionary subclass defines a default value method,
                # convert mapper to a lookup function (GH #15999).
                dict_with_default = mapper
                mapper = lambda x: dict_with_default[x]
            else:
                # Dictionary does not have a default. Thus it's safe to
                # convert to an Series for efficiency.
                # we specify the keys here to handle the
                # possibility that they are tuples

                # The return value of mapping with an empty mapper is
                # expected to be pd.Series(np.nan, ...). As np.nan is
                # of dtype float64 the return value of this method should
                # be float64 as well
                mapper = create_series_with_explicit_dtype(
                    mapper, dtype_if_empty=np.float64
                )

        if isinstance(mapper, ABCSeries):
            # Since values were input this means we came from either
            # a dict or a series and mapper should be an index
            if is_categorical_dtype(self._values):
                # use the built in categorical series mapper which saves
                # time by mapping the categories instead of all values
                return self._values.map(mapper)
            if is_extension_array_dtype(self.dtype):
                values = self._values
            else:
                values = self.values

            indexer = mapper.index.get_indexer(values)
            new_values = algorithms.take_1d(mapper._values, indexer)

            return new_values

        # we must convert to python types
        if is_extension_array_dtype(self.dtype) and hasattr(self._values, "map"):
            # GH#23179 some EAs do not have `map`
            values = self._values
            if na_action is not None:
                raise NotImplementedError
            map_f = lambda values, f: values.map(f)
        else:
            values = self.astype(object)
            values = getattr(values, "values", values)
            if na_action == "ignore":

                def map_f(values, f):
                    return lib.map_infer_mask(values, f, isna(values).view(np.uint8))

            else:
                map_f = lib.map_infer

        # mapper is a function
        new_values = map_f(values, mapper)

        return new_values
