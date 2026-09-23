    def map(self, mapper, na_action=None):
        """
        Map values using input correspondence (a dict, Series, or function).

        Parameters
        ----------
        mapper : function, dict, or Series
            Mapping correspondence.
        na_action : {None, 'ignore'}
            If 'ignore', propagate NA values, without passing them to the
            mapping correspondence.

        Returns
        -------
        applied : Union[Index, MultiIndex], inferred
            The output of the mapping function applied to the index.
            If the function returns a tuple with more than one element
            a MultiIndex will be returned.
        """

        from .multi import MultiIndex

        new_values = super()._map_values(mapper, na_action=na_action)

        attributes = self._get_attributes_dict()

        # we can return a MultiIndex
        if new_values.size and isinstance(new_values[0], tuple):
            if isinstance(self, MultiIndex):
                names = self.names
            elif attributes.get("name"):
                names = [attributes.get("name")] * len(new_values[0])
            else:
                names = None
            return MultiIndex.from_tuples(new_values, names=names)

        attributes["copy"] = False
        if not new_values.size:
            # empty
            attributes["dtype"] = self.dtype

        return Index(new_values, **attributes)
