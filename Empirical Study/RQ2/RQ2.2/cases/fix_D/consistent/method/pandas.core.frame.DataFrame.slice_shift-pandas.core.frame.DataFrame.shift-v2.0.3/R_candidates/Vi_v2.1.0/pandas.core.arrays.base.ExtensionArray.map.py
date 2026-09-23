    def map(self, mapper, na_action=None):
        """
        Map values using an input mapping or function.

        Parameters
        ----------
        mapper : function, dict, or Series
            Mapping correspondence.
        na_action : {None, 'ignore'}, default None
            If 'ignore', propagate NA values, without passing them to the
            mapping correspondence. If 'ignore' is not supported, a
            ``NotImplementedError`` should be raised.

        Returns
        -------
        Union[ndarray, Index, ExtensionArray]
            The output of the mapping function applied to the array.
            If the function returns a tuple with more than one element
            a MultiIndex will be returned.
        """
        return map_array(self, mapper, na_action=na_action)
