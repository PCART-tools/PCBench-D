    def map(self, mapper):
        """Apply mapper function to an index.

        Parameters
        ----------
        mapper : callable
            Function to be applied.

        Returns
        -------
        applied : Union[Index, MultiIndex], inferred
            The output of the mapping function applied to the index.
            If the function returns a tuple with more than one element
            a MultiIndex will be returned.

        """
        from .multi import MultiIndex
        mapped_values = self._arrmap(self.values, mapper)
        attributes = self._get_attributes_dict()
        if mapped_values.size and isinstance(mapped_values[0], tuple):
            return MultiIndex.from_tuples(mapped_values,
                                          names=attributes.get('name'))

        attributes['copy'] = False
        return Index(mapped_values, **attributes)
