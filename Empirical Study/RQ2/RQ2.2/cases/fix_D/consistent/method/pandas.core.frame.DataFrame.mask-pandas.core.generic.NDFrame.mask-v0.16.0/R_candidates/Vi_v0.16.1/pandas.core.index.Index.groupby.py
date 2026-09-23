    def groupby(self, to_groupby):
        """
        Group the index labels by a given array of values.

        Parameters
        ----------
        to_groupby : array
            Values used to determine the groups.

        Returns
        -------
        groups : dict
            {group name -> group labels}

        """
        return self._groupby(self.values, _values_from_object(to_groupby))
