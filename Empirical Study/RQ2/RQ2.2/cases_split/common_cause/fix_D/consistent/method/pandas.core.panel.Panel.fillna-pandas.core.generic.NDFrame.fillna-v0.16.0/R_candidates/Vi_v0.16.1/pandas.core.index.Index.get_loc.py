    def get_loc(self, key, method=None):
        """
        Get integer location for requested label

        Parameters
        ----------
        key : label
        method : {None, 'pad'/'ffill', 'backfill'/'bfill', 'nearest'}
            * default: exact matches only.
            * pad / ffill: find the PREVIOUS index value if no exact match.
            * backfill / bfill: use NEXT index value if no exact match
            * nearest: use the NEAREST index value if no exact match. Tied
              distances are broken by preferring the larger index value.

        Returns
        -------
        loc : int if unique index, possibly slice or mask if not
        """
        if method is None:
            return self._engine.get_loc(_values_from_object(key))

        indexer = self.get_indexer([key], method=method)
        if indexer.ndim > 1 or indexer.size > 1:
            raise TypeError('get_loc requires scalar valued input')
        loc = indexer.item()
        if loc == -1:
            raise KeyError(key)
        return loc
