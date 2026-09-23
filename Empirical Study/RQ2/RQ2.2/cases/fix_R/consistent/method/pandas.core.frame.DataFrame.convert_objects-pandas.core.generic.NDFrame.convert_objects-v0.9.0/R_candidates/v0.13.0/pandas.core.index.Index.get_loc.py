    def get_loc(self, key):
        """
        Get integer location for requested label

        Returns
        -------
        loc : int if unique index, possibly slice or mask if not
        """
        return self._engine.get_loc(_values_from_object(key))
