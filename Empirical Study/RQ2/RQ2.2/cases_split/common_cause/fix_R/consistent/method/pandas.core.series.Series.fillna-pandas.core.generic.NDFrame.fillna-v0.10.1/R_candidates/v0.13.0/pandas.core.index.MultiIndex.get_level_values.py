    def get_level_values(self, level):
        """
        Return vector of label values for requested level, equal to the length
        of the index

        Parameters
        ----------
        level : int

        Returns
        -------
        values : ndarray
        """
        num = self._get_level_number(level)
        unique_vals = self.levels[num]  # .values
        labels = self.labels[num]
        values = Index(com.take_1d(unique_vals.values, labels,
                                   fill_value=unique_vals._na_value))
        values.name = self.names[num]
        return values
